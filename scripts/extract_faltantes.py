"""Transcreve as 13 questoes faltantes da 1a fase (v2).

- 2003 (q11-14): itens marcados com os bullets Ø Ù Ú Û Ü (5 por questao).
- 2005 (q9-11, 15-17, 43): comando na margem da coluna, itens indentados
  (+37pt); questao multipla escolha (q43) vai com alternatives.
"""

import json
import re
import unicodedata
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
RE_MARK = re.compile(r"QUEST.{0,3}O\s*(\d{1,3})", re.I)
BULLETS = "ØÙÚÛÜ"
NOISE = re.compile(
    r"^(www\.|UnB / CESPE|Teste de Pr|É permitida|Admissão à Carreira|"
    r"Concurso de Admissão|Cargo:|–\s*\d+\s*–|Instituto Rio Branco|MINISTÉRIO)"
)


def norm(s: str) -> str:
    return " ".join(s.replace("\n", " ").split()).strip()


def read_lines(pdf: Path):
    out = []
    with pymupdf.open(pdf) as doc:
        for pno, pg in enumerate(doc, 1):
            for b in pg.get_text("dict")["blocks"]:
                for l in b.get("lines", []):
                    x0 = 1e9
                    words = []
                    for s in l["spans"]:
                        if s["text"].strip():
                            x0 = min(x0, s["bbox"][0])
                            words.append(s["text"].strip())
                    if words:
                        out.append(
                            (
                                pno,
                                round(l["bbox"][1], 1),
                                round(x0, 1),
                                unicodedata.normalize("NFC", " ".join(words)),
                            )
                        )
    # SEM sort por y: mantem a ordem natural do PDF (nao intercala colunas)
    return out


def extract_2003() -> list[dict]:
    pdf = ROOT / "data/raw/CACD_2003/archive/Primeira_Fase_Objetiva .pdf"
    with pymupdf.open(pdf) as doc:
        full = "".join(pg.get_text("text") for pg in doc)
        pages = {pno: pg.get_text("text") for pno, pg in enumerate(doc, 1)}
    marks = sorted((m.start(), int(m.group(1))) for m in RE_MARK.finditer(full))
    recs = []
    for qn in (11, 12, 13, 14):
        m0 = next(s for s, n in marks if n == qn)
        ends = [s for s, n in marks if s > m0 and n == qn + 1]
        end = ends[0] if ends else len(full)
        block = full[m0:end]
        # remove o rotulo "QUESTÃO N" do inicio do comando
        block = RE_MARK.sub("", block, count=1)
        page = next((pno for pno, t in pages.items() if f"QUESTÃO {qn}" in t), None)
        parts = re.split(rf"\s*[{''.join(BULLETS)}]\s*", block)
        recs.append(
            {
                "qn": qn,
                "page": page,
                "command": " ".join(parts[0].split()),
                "items": [norm(p) for p in parts[1:]],
            }
        )
    return recs


def extract_2005() -> list[dict]:
    pdf = ROOT / "data/raw/CACD_2005/archive/CESPE-2005-IRBR-Diplomata.pdf"
    lines = read_lines(pdf)
    wanted = (9, 10, 11, 15, 16, 17, 43)
    recs = []
    for qn in wanted:
        i0 = next(
            (
                i
                for i, (pno, y, x0, t) in enumerate(lines)
                if t.startswith(f"QUESTÃO {qn}")
            ),
            None,
        )
        if i0 is None:
            print(f"[!!] 2005 q{qn}: marcador nao encontrado")
            continue
        i1 = len(lines)
        for j in range(i0 + 1, len(lines)):
            if lines[j][3].startswith("QUESTÃO "):
                i1 = j
                break
        blk = [l for l in lines[i0:i1] if not NOISE.match(l[3])]
        col_left = min(x for _, _, x, _ in blk)
        command_lines, item_lines = [], []
        for pno, y, x0, t in blk:
            if t.startswith(f"QUESTÃO {qn}"):
                continue
            (command_lines if x0 <= col_left + 12 else item_lines).append(
                (pno, y, x0, t)
            )
        items, buf = [], []
        for pno, y, x0, t in item_lines:
            if (
                buf
                and re.search(r"\.\s*$", buf[-1][3])
                and re.match(r"^[A-ZÀ-Ú(“\"]", t)
            ):
                items.append(norm(" ".join(b[3] for b in buf)))
                buf = [(pno, y, x0, t)]
            else:
                buf.append((pno, y, x0, t))
        if buf:
            items.append(norm(" ".join(b[3] for b in buf)))
        command = norm(" ".join(c[3] for c in command_lines))
        recs.append({"qn": qn, "page": blk[0][0], "command": command, "items": items})
    return recs


def emit(records: list[dict], contest: str, year: int, src: str):
    # correcoes pontuais 2005 (blocos de duas colunas que misturaram cabecalho
    # de texto/ citacao nos itens) — texto conferido no PDF
    FIXES = {
        10: {
            "command": (
                "Na segunda metade do século XIX, o imperialismo — inclusive por sua "
                "vertente neocolonialista — atesta o grau de desenvolvimento do capitalismo "
                "e sua incessante busca de conquista dos mercados mundiais. A respeito desse "
                "processo de expansão, julgue (C ou E) os itens seguintes."
            ),
            "drop_first": True,
        },
        11: {
            "command": (
                "Com o auxílio do texto III, julgue (C ou E) os itens seguintes, "
                "considerando o século XIX como o laboratório em que foi gerado o século XX, "
                "a despeito das singularidades de cada um dos períodos."
            ),
            "drop_first": True,
        },
        17: {
            "command": (
                "Tendo em vista a realidade histórica mundial contemporânea e a base teórica "
                "do Estado do pós-guerra nos países desenvolvidos, julgue os itens seguintes."
            ),
            "drop_first": False,
        },
    }
    out = ROOT / "data/raw" / f"CACD_{year}" / "archive" / "questoes_faltantes.jsonl"
    n = 0
    with out.open("w", encoding="utf-8") as fh:
        for r in records:
            if contest == "CACD_2005" and r["qn"] == 43:
                # multipla escolha: enunciado + alternatives A-E, itn=null
                alts = " ".join(f"{'ABCDE'[i]}) {t}" for i, t in enumerate(r["items"]))
                fh.write(
                    json.dumps(
                        {
                            "contest_id": contest,
                            "year": year,
                            "phase": 1,
                            "stage": "primeira_fase",
                            "discipline": None,
                            "question_number": r["qn"],
                            "item_number": None,
                            "question_type": "multiple_choice",
                            "question_text": r["command"],
                            "item_text": None,
                            "alternatives": alts,
                            "answer": None,
                            "page": r["page"],
                            "caderno": None,
                            "source_file": src,
                            "source_url": None,
                            "confidence": 0.85,
                            "notes": "transcricao automatica do PDF archive.org (questao faltante no manual)",
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
                n += 1
                continue
            fix = FIXES.get(r["qn"], {}) if contest == "CACD_2005" else {}
            items = list(r["items"])
            if fix.get("drop_first"):
                items = items[1:]
            # linhas de furniture das provas 2003-2010 (não são itens)
            items = [
                i
                for i in items
                if not re.match(
                    r"^(Texto IV|Texto \w+ ?–|J\. M\.|J\. J\.|Enrique|Extensão máxima|"
                    r"\(valor da questão|In ? :|O século XX –|www\.)",
                    i,
                )
            ]
            for itn, item in enumerate(items, 1):
                fh.write(
                    json.dumps(
                        {
                            "contest_id": contest,
                            "year": year,
                            "phase": 1,
                            "stage": "primeira_fase",
                            "discipline": None,
                            "question_number": r["qn"],
                            "item_number": itn,
                            "question_type": "certo_errado",
                            "question_text": fix.get("command") or r["command"],
                            "item_text": item,
                            "alternatives": None,
                            "answer": None,
                            "page": r["page"],
                            "caderno": None,
                            "source_file": src,
                            "source_url": None,
                            "confidence": 0.85,
                            "notes": "transcricao automatica do PDF archive.org (questao faltante no manual)",
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
                n += 1
    print(f"[ok] {contest}: {len(records)} questoes, {n} registros -> {out.name}")


if __name__ == "__main__":
    r03 = extract_2003()
    r05 = extract_2005()
    for rec in r03:
        print(
            f"2003 q{rec['qn']} pg{rec['page']}: {len(rec['items'])} itens | cmd: {rec['command'][:50]!r}"
        )
        for i, it in enumerate(rec["items"], 1):
            print(f"    {i}: {it[:75]!r}")
    print()
    for rec in r05:
        print(
            f"2005 q{rec['qn']} pg{rec['page']}: {len(rec['items'])} itens | cmd: {rec['command'][:50]!r}"
        )
        for i, it in enumerate(rec["items"], 1):
            print(f"    {i}: {it[:75]!r}")
    emit(
        r03, "CACD_2003", 2004, "data/raw/CACD_2003/archive/Primeira_Fase_Objetiva .pdf"
    )
    emit(
        r05,
        "CACD_2005",
        2005,
        "data/raw/CACD_2005/archive/CESPE-2005-IRBR-Diplomata.pdf",
    )
