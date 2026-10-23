"""Extrai as questoes discursivas/escritas 2013-2016 (wayback + secundario).

- Cada arquivo = prova escrita de uma disciplina ('PROVA ESCRITA DE <X>').
- Blocos 'QUESTAO N' -> registros; classificacao:
  * bloco com 'Extensao maxima'/'[valor' => essay (dissertativa, itn=null)
  * bloco com opcoes numeradas 1-4 => multiple_choice (alternatives)
  * outros => certo_errado (C/E, itn=null)
- Stage: LP/LI => segunda_fase; demais => terceira_fase.
"""

import glob
import json
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
sys_dir = str(ROOT)
if sys_dir not in sys.path:
    sys.path.insert(0, sys_dir)

from parser.parsers.base import DISCIPLINE_NORMALIZE  # noqa: E402

RE_Q = re.compile(r"QUEST[ÃA]O\s+(\d{1,2})", re.I)
RE_SUBJ = re.compile(r"PROVA ESCRITA DE ([A-ZÀ-Ú ]{3,80})", re.I)
RE_ESSAY = re.compile(r"Extens[ãa]o m[áa]xima|valor da quest[ãa]o", re.I)


def norm(s: str) -> str:
    return " ".join(s.replace("\n", " ").split()).strip()


def read_pdf(p: Path) -> str:
    with pymupdf.open(p) as doc:
        return "\n".join(pg.get_text("text") for pg in doc)


def extract_file(pdf: Path, disc_default: str | None, stage: str) -> list[dict]:
    full = read_pdf(pdf)
    evs = []
    for m in re.finditer(r"PROVA ESCRITA DE ([A-ZÀ-Ú ]{3,80})", full):
        d = DISCIPLINE_NORMALIZE.get(m.group(1).strip().upper())
        if d:
            evs.append((m.start(), "S", d))
    for m in RE_Q.finditer(full):
        evs.append((m.start(), "Q", int(m.group(1))))
    evs.sort(key=lambda e: e[0])
    recs = []
    for idx, (pos, kind, val) in enumerate(evs):
        if kind == "S":
            continue
        disc = next(
            (v2 for p2, k2, v2 in reversed(evs[:idx]) if k2 == "S"), disc_default
        )
        if disc is None:
            continue
        nxt = evs[idx + 1][0] if idx + 1 < len(evs) else len(full)
        body = norm(full[pos:nxt])
        if not body or len(body) < 40:
            continue
        qtype = "essay" if RE_ESSAY.search(body) else "certo_errado"
        recs.append(
            {
                "contest_id": f"CACD_{year_of(pdf)}",
                "year": year_of(pdf),
                "phase": 2 if stage == "segunda_fase" else 3,
                "stage": stage,
                "discipline": disc,
                "question_number": val,
                "item_number": None,
                "question_type": qtype,
                "question_text": body,
                "item_text": None,
                "alternatives": None,
                "answer": None,
                "page": None,
                "caderno": None,
                "source_file": str(pdf.relative_to(ROOT)).replace("\\", "/"),
                "source_url": None,
                "confidence": 0.8,
                "notes": "extracao automatica (wayback/secondary), revisar",
            }
        )
    return recs


def year_of(pdf: Path) -> int:
    return int(re.search(r"CACD_(\d{4})", str(pdf)).group(1))


SUBJ_MAP = {
    "LÍNGUA PORTUGUESA": "Língua Portuguesa",
    "LÍNGUA INGLESA": "Língua Inglesa",
    "LÍNGUA ESPANHOLA": "Espanhol e Francês",
    "LÍNGUA FRANCESA": "Espanhol e Francês",
    "LÍNGUA ESPANHOLA E LÍNGUA FRANCESA": "Espanhol e Francês",
    "HISTÓRIA DO BRASIL": "História do Brasil",
    "GEOGRAFIA": "Geografia",
    "GEOGRAFIA E POLÍTICA INTERNACIONAL": "Geografia e Política Internacional",
    "POLÍTICA INTERNACIONAL E GEOGRAFIA": "Geografia e Política Internacional",
    "POLÍTICA INTERNACIONAL": "Política Internacional",
    "NOÇÕES DE ECONOMIA": "Economia",
    "NOÇÕES DE DIREITO E DIREITO INTERNACIONAL PÚBLICO": "Direito",
    "NOÇÕES DE DIREITO": "Direito",
    "DIREITO INTERNACIONAL PÚBLICO": "Direito",
}

E2 = {"essay": "essay"}


def main() -> None:
    for y in (2013, 2014, 2015, 2016):
        pdfs = sorted(
            glob.glob(f"data/raw/CACD_{y}/**/prova_discursiva*.pdf", recursive=True)
        ) + sorted(glob.glob(f"data/raw/CACD_{y}/**/discursiva_*.pdf", recursive=True))
        recs = []
        for p in pdfs:
            pp = Path(p)
            full = read_pdf(Path(p))
            m = re.search(r"PROVA ESCRITA DE ([A-ZÀ-Ú ]{3,80})", full)
            raw_subj = m.group(1).strip().upper() if m else None
            disc = SUBJ_MAP.get(raw_subj)
            stage = (
                "segunda_fase"
                if disc in ("Língua Portuguesa", "Língua Inglesa")
                else "terceira_fase"
            )
            recs.extend(extract_file(Path(p), disc, stage))
        # dedup por (stage, disciplina, questao): o mesmo conteudo aparece em
        # 2 arquivos (prova_discursiva + discursiva_<materia>)
        vistos, unicos = set(), []
        for r in recs:
            k = (r["stage"], r["discipline"], r["question_number"])
            if k not in vistos:
                vistos.add(k)
                unicos.append(r)
        recs = unicos
        out = ROOT / "data/raw" / f"CACD_{y}" / f"discursivas1316_{y}.jsonl"
        with out.open("w", encoding="utf-8") as fh:
            for r in recs:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        by_stage = {}
        for r in recs:
            by_r = f"{r['stage']}/{r['discipline'] or '?'}"
            by_stage[
                by_r := by_stage.get(
                    by_r := by_stage
                    and by_r
                    or r["stage"] + "/" + str(r["discipline"]),
                    0,
                )
            ] = 1
        print(f"[ok] {out.name}: {len(recs)} registros")


def extract_file(pdf: Path, disc: str | None, stage: str) -> list[dict]:
    full = read_pdf(pdf)
    evs = []
    for m in re.finditer(
        r"^\s*(?:(?:TERCEIRA|SEGUNDA) FASE\s*[–-]\s*)?PROVA\s+(?:ESCRITA\s+DE|DE)\s+([A-Za-zÀ-ú ]{3,90}?)\s*$",
        full,
        re.M | re.I,
    ):
        d = SUBJ_MAP.get(m.group(1).strip().upper())
        if d:
            evs.append((m.start(), "S", d))
    for m in RE_Q.finditer(full):
        evs.append((m.start(), "Q", int(m.group(1))))
    evs.sort(key=lambda e: e[0])
    recs = []
    for idx, (pos, kind, val) in enumerate(evs):
        if kind == "S":
            continue
        disc = next((v2 for p2, k2, v2 in reversed(evs[:idx]) if k2 == "S"), disc)
        if disc is None:
            continue
        nxt = evs[idx + 1][0] if idx + 1 < len(evs) else len(full)
        body = norm(full[pos:nxt])
        if len(body) < 40:
            continue
        is_essay = bool(
            re.search(r"Extens[ãa]o m[áa]xima|valor da quest[ãa]o", body, re.I)
        )
        recs.append(
            {
                "contest_id": f"CACD_{year_of(pdf)}",
                "year": year_of(pdf),
                "phase": 2 if stage == "segunda_fase" else 3,
                "stage": stage,
                "discipline": disc,
                "question_number": val,
                "item_number": None,
                "question_type": "essay" if is_essay else "certo_errado",
                "question_text": body,
                "item_text": None,
                "alternatives": None,
                "answer": None,
                "page": None,
                "caderno": None,
                "source_file": str(pdf).replace("\\", "/"),
                "source_url": None,
                "confidence": 0.8,
                "notes": "extracao automatica (wayback/secondary)",
            }
        )
    return recs


def year_of(pdf) -> int:
    m = re.search(r"CACD_(\d{4})", str(pdf))
    return int(m.group(1))


if __name__ == "__main__":
    main()
