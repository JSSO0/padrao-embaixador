"""Extrai as provas objetivas 2025/2026 (formato Cebraspe novo, sem "Questao N")
pelo TEXTO LINEAR dos PDFs oficiais (a ordem nativa dos PDFs Cebraspe 2024+
e a ordem de leitura correta; confirmado por probes em probes descartados).

Estrutura confirmada:
- cada item aparece como "<num> <comando>" (inline) ou "<num>" em linha
  propria (standalone; itens 1-9 do caderno), com o comando nas linhas
  seguintes ate: linha em branco, proximo item, cabecalho de pagina
  ("CEBRASPE ...") ou titulo de secao;
- textos-base, citacoes e instrucoes ("Julgue os itens...") acumulam em
  buffer e vinculam ao PRIMEIRO item do bloco (mesmo formato do extrator
  anterior: contexto + comando no 1o item, so o enunciado nos seguintes);
- a disciplina vem do titulo de secao em linha propria (ALL CAPS);

NAO rode pipeline/extract_objetivas_2015_2018.py para 2025/2026: ele nao
entende este formato e sobrescreveria estes JSONLs com saida parcial.

Uso:
    python pipeline/extract_cebraspe_linear.py             # 2025 e 2026
    python pipeline/extract_cebraspe_linear.py --year 2025
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from parser.parsers.base import DISCIPLINE_NORMALIZE, is_section_header  # noqa: E402

RAW = ROOT / "data" / "raw"

RE_STANDALONE = re.compile(r"^(\d{1,3})$")
RE_INLINE = re.compile(r"^(\d{1,3})\s+([^\s\d].*)$")
RE_PAGE_HEADER = re.compile(r"^CEBRASPE\b")

FIELDS = [
    "contest_id",
    "year",
    "phase",
    "stage",
    "discipline",
    "question_number",
    "item_number",
    "question_type",
    "question_text",
    "item_text",
    "alternatives",
    "answer",
    "page",
    "caderno",
    "source_file",
    "source_url",
    "confidence",
    "notes",
]


def get_lines(pdf: Path):
    doc = pymupdf.open(pdf)
    out = []
    for pno, page in enumerate(doc, 1):
        for raw in page.get_text("text").split("\n"):
            out.append((pno, unicodedata.normalize("NFC", raw.strip())))
    doc.close()
    return out


def section_of(t: str) -> str | None:
    s = is_section_header(t)
    if not s:
        return None
    return DISCIPLINE_NORMALIZE.get(s)  # titulo desconhecido (ex. TEXTO II) -> None


def item_start(t: str, expected: int | None):
    """Retorna (num, resto_do_comando) se a linha inicia o item esperado."""
    inline = False
    m = RE_STANDALONE.match(t)
    if m:
        n = int(m.group(1))
    else:
        m = RE_INLINE.match(t)
        if not m:
            return None, None
        n = int(m.group(1))
        inline = True
    ok = (expected is not None and n == expected) or (
        expected is None and 1 <= n <= 150
    )
    if not ok:
        return None, None
    return n, (m.group(2) if inline else None)


def parse_pdf(pdf: Path) -> dict[int, dict]:
    lines = get_lines(pdf)
    # descarta a capa (tudo ate a linha "PROVA OBJETIVA")
    for i, (pno, t) in enumerate(lines):
        if t.upper().startswith("PROVA OBJETIVA"):
            lines = lines[i + 1 :]
            break

    items: dict[int, dict] = {}
    st = {"expected": None, "cur": None, "pending": [], "disc": None}

    def close() -> None:
        cur = st["cur"]
        if cur is None:
            return
        q = items[cur]
        q["text"] = " ".join(" ".join(q["parts"]).split())
        st["cur"] = None

    for pno, t in lines:
        if not t:
            cur = st["cur"]
            # linha em branco encerra o comando do item em curso
            if cur is not None and items[cur]["parts"]:
                close()
            continue
        if (
            RE_PAGE_HEADER.match(t)
            or t.startswith("--")
            or t.upper().startswith("PROVA OBJETIVA")
        ):
            continue
        sec = section_of(t)
        if sec:
            close()
            st["disc"] = sec
            st["pending"] = []
            continue
        n, rest = item_start(t, st["expected"])
        if n is not None:
            close()
            st["cur"] = n
            ctx = " ".join(st["pending"]).strip()
            st["pending"] = []
            items[n] = {
                "page": pno,
                "disc": st["disc"],
                "ctx": ctx,
                "parts": [rest] if rest else [],
            }
            st["expected"] = n + 1
            continue
        cur = st["cur"]
        if cur is not None:
            items[cur]["parts"].append(t)
        else:
            st["pending"].append(t)
    close()

    out = {}
    for n, q in items.items():
        text = " ".join(" ".join(q["parts"]).split())
        out[n] = {
            "page": q["page"],
            "discipline": q["disc"],
            "question_text": (q["ctx"] + " " + text).strip() if q["ctx"] else text,
        }
    return out


def report(tag: str, items: dict[int, dict]) -> None:
    if not items:
        print(f"[!!] {tag}: nenhum item extraido")
        return
    ns = sorted(items)
    missing = [n for n in range(ns[0], ns[-1] + 1) if n not in items]
    discs: dict[str, int] = {}
    for q in items.values():
        d = q["discipline"] or "None"
        discs[d] = discs.get(d, 0) + 1
    print(
        f"[ok] {tag}: {len(items)} itens | faixa {ns[0]}-{ns[-1]} | faltando: {missing}"
    )
    print("     disciplinas:", dict(sorted(discs.items())))
    no_disc = [n for n in ns if items[n]["discipline"] is None]
    if no_disc:
        print("     [!!] sem disciplina:", no_disc[:20])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, action="append")
    args = ap.parse_args()
    years = args.year or [2025, 2026]

    for year in years:
        folder = RAW / f"CACD_{year}" / "cebraspe"
        pdfs = sorted(folder.glob("prova_objetiva*.pdf"))
        total = 0
        for i, pdf in enumerate(pdfs, 1):
            items = parse_pdf(pdf)
            total += len(items)
            out = folder / f"cacd_{year}_primeira_fase_prova_objetiva_{i}.jsonl"
            contest = f"CACD_{year}"
            src = str(pdf.relative_to(ROOT)).replace("\\", "/")
            with out.open("w", encoding="utf-8") as fh:
                for n in sorted(items):
                    q = items[n]
                    rec = {
                        "contest_id": contest,
                        "year": year,
                        "phase": 1,
                        "stage": "primeira_fase",
                        "discipline": q["discipline"],
                        "question_number": n,
                        "item_number": None,
                        "question_type": "certo_errado",
                        "question_text": q["question_text"],
                        "item_text": None,
                        "alternatives": None,
                        "answer": None,
                        "page": q["page"],
                        "caderno": None,
                        "source_file": src,
                        "source_url": None,
                        "confidence": 0.95,
                        "notes": None,
                    }
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            report(f"{out.name}", items)
        print(f"== {year}: {len(pdfs)} provas, {total} itens")


if __name__ == "__main__":
    main()
