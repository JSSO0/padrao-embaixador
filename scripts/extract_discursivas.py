"""Extrai as questoes discursivas da 2a/3a fase (era Cebraspe) dos PDFs
prova_discursiva + o PADRAO DE RESPOSTA oficial como answer; e as provas
discursivas por disciplina (2019-2023, 3a fase) do repositorio secundario.

Formatos:
- provas: cabecalho '-- PROVA ESCRITA DE <DISCIPLINA> --' (travessoes
  opcionais) e blocos 'QUESTAO N' (qualquer capitalizacao);
- padroes 2024+: 'Prova Escrita de <X> - Questao N' + o corpo da resposta;
- padroes 2017-2018: 'PROVA DISCURSIVA|ESCRITA - SEGUNDA/TERCEIRA FASE' +
  '<DISCIPLINA> - QUESTAO N' (o subject pode quebrar linha) ou '... -
  REDACAO/RESUMO/SUMMARY' (mkept como qn 1/2);
- provas por disciplina (2019-2023): arquivos discursiva_<materia>__*.pdf,
  4 questoes cada, extraidos como terceira fase.
"""

import json
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from parser.parsers.base import DISCIPLINE_NORMALIZE  # noqa: E402

RE_SUBJECT = re.compile(
    r"^\s*-{0,2}\s*PROVA\s+ESCRITA\s+DE\s+(.+?)\s*-{0,2}\s*$", re.M | re.I
)
RE_Q = re.compile(r"QUEST[ÃA]O\s+(\d{1,2})", re.I)
RE_PR_HEAD = re.compile(
    r"Prova\s+Escrita\s+de\s+([A-Za-zÀ-Ú ]+?)\s*[–-]\s*Quest[ãa]o\s+(\d{1,2})", re.I
)
RE_FASE = re.compile(r"PROVA (DISCURSIVA|ESCRITA)\s*[–-]\s*(SEGUNDA|TERCEIRA) FASE")
RE_MARKER_LINE = re.compile(
    r"(.{3,80}?)\s*[–-]\s*(QUEST[ÃA]O\s+(\d{1,2})|REDAÇÃO|RESUMO|SUMMARY)", re.I
)
JUNK_LINE = re.compile(
    r"^(Aplicação|PADRÃO DE RESPOSTA|CESPE|CEBRASPE|INSTITUTO|MINISTÉRIO|CONCURSO|CARGO)\b|^\d+$",
    re.I,
)


def norm_text(s: str) -> str:
    return " ".join(s.split())


def read_pdf(p: Path) -> str:
    with pymupdf.open(p) as doc:
        return "\n".join(pg.get_text("text") for pg in doc)


def extract_prova(pdf: Path) -> dict[tuple[str, int], str]:
    """{(disciplina, qn): enunciado} — era Cebraspe."""
    out: dict[tuple[str, int], str] = {}
    full = read_pdf(pdf)
    evs: list[tuple[int, str, object]] = []
    for m in RE_SUBJECT.finditer(full):
        disc = DISCIPLINE_NORMALIZE.get(m.group(1).strip().upper())
        if disc:
            evs.append((m.start(), "S", disc))
    for m in RE_Q.finditer(full):
        evs.append((m.start(), "Q", int(m.group(1))))
    evs.sort(key=lambda e: e[0])
    for idx, (pos, kind, val) in enumerate(evs):
        if kind == "S":
            continue
        disc = next((v2 for p2, k2, v2 in reversed(evs[:idx]) if k2 == "S"), None)
        if disc is None:
            continue
        nxt = evs[idx + 1][0] if idx + 1 < len(evs) else len(full)
        body = RE_Q.sub("", full[pos:nxt])
        out.setdefault((disc, val), norm_text(body))
    return out


def extract_padrao_novo(pdf: Path) -> dict[tuple[str, int], str]:
    """Formato 2024+: 'Prova Escrita de <X> - Questao N' + corpo."""
    out: dict[tuple[str, int], str] = {}
    full = norm_text(read_pdf(pdf))
    heads = sorted(
        (m.start(), m.group(1).strip().upper(), int(m.group(2)))
        for m in RE_PR_HEAD.finditer(full)
    )
    for idx, (pos, disc_raw, qn) in enumerate(heads):
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(full)
        disc = DISCIPLINE_NORMALIZE.get(disc_raw.upper())
        body = norm_text(RE_PR_HEAD.sub("", full[pos:end], count=1))
        if disc:
            out.setdefault((disc, qn), body)
    return out


def extract_padrao_antigo(pdf: Path) -> dict[tuple[str, int], str]:
    """Formato 2017-2018: linhas 'PROVA DISCURSIVA|ESCRITA - SEGUNDA/TERCEIRA
    FASE' seguidas de '<DISCIPLINA> - QUESTAO N' (subject pode quebrar linha)
    ou '<DISCIPLINA> - REDACAO|RESUMO|SUMMARY' (marcador sem numero)."""
    out: dict[tuple[str, int], str] = {}
    lines = [ln.strip() for ln in read_pdf(pdf).split("\n") if ln.strip()]
    blocks: list[tuple[int, str, int]] = []  # (marker_idx, disc, qn)
    disc = None
    for idx, ln in enumerate(lines):
        if re.fullmatch(
            r"PROVA (DISCURSIVA|ESCRITA)\s*[–-]\s*(SEGUNDA|TERCEIRA) FASE", ln
        ):
            continue
        m = re.fullmatch(r"(.{3,90}?)\s*[–-]\s*QUEST[ÃA]O\s+(\d{1,2})", ln)
        if m:
            d = (
                DISCIPLINE_NORMALIZE.get(m.group(1).strip().upper())
                or m.group(1).title()
            )
            blocks.append((idx, d, int(m.group(2))))
            disc = None
            continue
        m2 = re.fullmatch(
            r"([A-Za-zÀ-Ú ]{3,90}?)\s*[–-]\s*(REDAÇÃO|RESUMO|SUMMARY)", ln
        )
        if m2:
            d = (
                DISCIPLINE_NORMALIZE.get(m2.group(1).strip().upper())
                or m2.group(1).title()
            )
            qn = {"REDAÇÃO": 1, "SUMMARY": 1, "RESUMO": 1}.get(m2.group(2).upper(), 1)
            blocks.append((idx, d, qn))
            disc = None
            continue
        m3 = re.fullmatch(r"([A-Za-zÀ-Ú ]{3,90}?)\s*[–-]", ln)
        if m3 and idx + 1 < len(lines) and re.search(r"QUEST[ÃA]O \d", lines[idx + 1]):
            disc = (
                DISCIPLINE_NORMALIZE.get(m3.group(1).strip().upper())
                or m3.group(1).title()
            )
            continue
        if disc and re.fullmatch(r"QUEST[ÃA]O\s+(\d{1,2})", ln):
            qn = int(re.fullmatch(r"QUEST[ÃA]O\s+(\d{1,2})", ln).group(1))
            blocks.append((idx, disc, qn))
            disc = None
    for bidx, (midx, disc, qn) in enumerate(blocks):
        body_start = midx + 1
        body_end = blocks[bidx + 1][0] if bidx + 1 < len(blocks) else len(lines)
        body = " ".join(
            ln for ln in lines[body_start:body_end] if not JUNK_LINE.match(ln)
        )
        if disc and len(body) > 60:
            out.setdefault((disc, qn), norm_text(body))
    return out


def extract_subject_prova(pdf: Path, disc: str) -> dict[tuple[str, int], str]:
    """Prova discursiva de uma unica disciplina (2019-2023)."""
    out: dict[tuple[str, int], str] = {}
    full = read_pdf(pdf)
    qs = sorted((m.start(), int(m.group(1))) for m in RE_Q.finditer(full))
    for idx, (pos, qn) in enumerate(qs):
        end = qs[idx + 1][0] if idx + 1 < len(qs) else len(full)
        body = RE_Q.sub("", full[pos:end])
        out.setdefault((disc, qn), norm_text(body))
    return out


def main() -> None:
    # 1) 2a fase (era Cebraspe): prova_discursiva + padrao_resposta
    for year in [2017, 2018, 2024, 2025, 2026]:
        folder = ROOT / "data/raw" / f"CACD_{year}" / "cebraspe"
        if not folder.exists():
            continue
        provas: dict[tuple[str, int], str] = {}
        padroes: dict[tuple[str, int], str] = {}
        for p in sorted(folder.glob("prova_discursiva*.pdf")):
            for k, v in extract_prova(p).items():
                provas.setdefault(k, v)
        for p in sorted(folder.glob("padrao_resposta*.pdf")):
            merged = extract_padrao_novo(p)
            for k, v in extract_padrao_antigo(p).items():
                merged.setdefault(k, v)
            for k, v in merged.items():
                padroes.setdefault(k, v)
        recs = []
        for key in sorted(provas, key=lambda k: (k[0], k[1])):
            disc, qn = key
            recs.append(
                {
                    "contest_id": f"CACD_{year}",
                    "year": year,
                    "phase": 2,
                    "stage": "segunda_fase",
                    "discipline": disc,
                    "question_number": qn,
                    "item_number": None,
                    "question_type": "essay",
                    "question_text": provas[key],
                    "item_text": None,
                    "alternatives": None,
                    "answer": padroes.get(key),
                    "page": None,
                    "caderno": None,
                    "source_file": f"data/raw/CACD_{year}/cebraspe/",
                    "source_url": None,
                    "confidence": 0.85,
                    "notes": None,
                }
            )
        out = folder / f"discursivas_{year}.jsonl"
        with out.open("w", encoding="utf-8") as fh:
            for r in recs:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        com_pr = sum(1 for r in recs if r["answer"])
        print(f"[ok] {out.name}: {len(recs)} questoes | com padrao: {com_pr}")

    # 2) 3a fase (2019-2023): provas discursivas por disciplina
    for year in [2019, 2020, 2022, 2023]:
        folder = next(
            (
                f
                for f in [
                    ROOT / "data/raw" / f"CACD_{year}",
                    ROOT / "data/raw" / f"CACD_{year}_{year + 1}",
                ]
                if f.exists()
            ),
            None,
        )
        if folder is None:
            continue
        contest = folder.name
        pdfs = sorted(folder.rglob("discursiva_*.pdf"))
        subj_map = {
            "DIREITO": "Direito",
            "HISTORIA": "História do Brasil",
            "ECONOMIA": "Economia",
            "GEOGRAFIA": "Geografia",
            "INGLES": "Língua Inglesa",
            "POLITICA_INTERNACIONAL": "Política Internacional",
            "PORTUGUES": "Língua Portuguesa",
            "ESPANHOL_FRANCES": "Espanhol e Francês",
        }
        recs = []
        for p in pdfs:
            m = re.match(r"discursiva_([a-z_]+)", p.name)
            if not m:
                continue
            disc = subj_map.get(m.group(1).strip("_").upper())
            if not disc:
                continue
            for (d2, qn), text in extract_subject_prova(p, disc).items():
                recs.append(
                    {
                        "contest_id": folder.name,
                        "year": year,
                        "phase": 3,
                        "stage": "terceira_fase",
                        "discipline": d2,
                        "question_number": qn,
                        "item_number": None,
                        "question_type": "essay",
                        "question_text": text,
                        "item_text": None,
                        "alternatives": None,
                        "answer": None,
                        "page": None,
                        "caderno": None,
                        "source_file": str(p.relative_to(ROOT)).replace("\\", "/"),
                        "source_url": None,
                        "confidence": 0.7,
                        "notes": "extracao automatica do repositorio secundario",
                    }
                )
        out = folder / f"discursivas3f_{year}.jsonl"
        with out.open("w", encoding="utf-8") as fh:
            for r in recs:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"[ok] {out.name}: {len(recs)} questoes de 3a fase")


if __name__ == "__main__":
    main()
