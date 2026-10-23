"""Fase 3 — provas escritas por disciplina 2005-2012 (era zips).

Extrai os PDFs de prova escrita por disciplina dos zips do archive.org e
emite registros no formato manual. O subject vem do nome do arquivo
(discursiva_<materia> ou IRBr_<MATERIA>). A fase vem do nome quando
declarada (2a/3a/4a), default segunda_fase para a era pre-2013.
"""

import json
import re
import sys
import zipfile
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from parser.parsers.base import DISCIPLINE_NORMALIZE  # noqa: E402

RE_Q = re.compile(r"QUEST[ÃA]O\s+(\d{1,2})", re.I)
SUBJ_MAP = {
    "DIREITO": "Direito",
    "HISTORIA DO BRASIL": "História do Brasil",
    "HIST_DO_BRASIL": "História do Brasil",
    "HISTORIA": "História do Brasil",
    "ECONOMIA": "Economia",
    "NOCOES_DE_ECONOMIA": "Economia",
    "GEOGRAFIA": "Geografia",
    "INGLES": "Língua Inglesa",
    "INGLES_3A_FASE": "Língua Inglesa",
    "POLITICA INTERNACIONAL": "Política Internacional",
    "POLIT_INTERNAC": "Política Internacional",
    "PORTUGUES": "Língua Portuguesa",
    "ESPANHOL": "Espanhol e Francês",
    "FRANCES": "Espanhol e Francês",
    "ALEMAO": "Alemão",
}


def norm(s: str) -> str:
    return " ".join(s.replace("\n", " ").split()).strip()


def read_pdf(p: Path) -> str:
    with pymupdf.open(p) as doc:
        return "\n".join(pg.get_text("text") for pg in doc)


def extract_prova_escrita(pdf: Path, disc: str, stage: str, phase: int):
    """Blocos QUESTAO N de prova escrita por disciplina."""
    out: dict[tuple[str, int], str] = {}
    full = read_pdf(pdf)
    qs = sorted(
        (m.start(), int(m.group(1)))
        for m in re.finditer(r"QUEST[ÃA]O\s+(\d{1,2})", full)
    )
    for idx, (pos, qn_) in enumerate(qs):
        end = qs[idx + 1][0] if idx + 1 < len(qs) else len(full)
        body = norm(re.sub(r"QUEST[ÃA]O\s+\d+", "", full[pos:end], count=1))
        if len(body) < 60:
            continue
        out.setdefault((disc, qn_), body)
    return out


def main() -> None:
    total = 0
    for y in range(2003, 2013):
        folder = next(
            (
                f
                for f in [
                    ROOT / "data/raw" / f"CACD_{y}",
                    ROOT / "data/raw" / f"CACD_{y}_{y + 1}",
                ]
                if f.exists()
            ),
            None,
        )
        if folder is None:
            continue
        zips = sorted(folder.rglob("*.zip"))
        if not zips:
            continue
        recs = []
        for zpath in zips:
            with __import__("zipfile").ZipFile(zpath) as zf:
                for name in zf.namelist():
                    if not re.search(
                        r"(?i)(escr|prova escrita|escrita)", Path(name).name
                    ) and not re.search(
                        r"IRBR_(DIREITO|ECONOMIA|ESPANHOL|FRANCES|GEOGRAFIA|HISTORIA DO BRASIL|INGLES|POLIT_INTERNAC|PORTUGUES|DIREITO_INTERNACIONAL)",
                        Path(name).stem,
                    ):
                        continue
                    if Path(name).suffix.lower() != ".pdf":
                        continue
                    # extrai temporariamente
                    dest = zpath.parent / Path(name).name
                    if not dest.exists():
                        dest.write_bytes(
                            __import__("zipfile").ZipFile(zpath).read(name)
                        )
                    # subject pelo nome do arquivo
                    stem = Path(name).stem
                    raw = stem
                    disc = None
                    for pat, cand in [
                        (r"NOCOES_DE_ECONOMIA|ECONOMIA", "Economia"),
                        (
                            r"HIST_DO_BRASIL|HISTORIA DO BRASIL|HISTORIA",
                            "História do Brasil",
                        ),
                        (r"GEOGRAFIA", "Geografia"),
                        (
                            r"POLITICA INTERNACIONAL|POLIT_INTERNAC|DIREITO_INTERNACIONAL_PUBLICO",
                            "Direito",
                        ),
                        (r"INGLES", "Língua Inglesa"),
                        (r"PORTUGUES", "Língua Portuguesa"),
                        (r"ESPANHOL|FRANCES", "Espanhol e Francês"),
                    ]:
                        if re.search(pat, stem.upper()):
                            disc = cand
                            break
                    if disc is None:
                        continue
                    for (d2, qn_), body in extract_prova_escrita(
                        dest, disc, "segunda_fase", 2
                    ).items():
                        recs.append(
                            {
                                "contest_id": folder.name,
                                "year": int(y),
                                "phase": 2,
                                "stage": "segunda_fase",
                                "discipline": d2,
                                "question_number": qn_,
                                "item_number": None,
                                "question_type": "essay",
                                "question_text": body,
                                "item_text": None,
                                "alternatives": None,
                                "answer": None,
                                "page": None,
                                "caderno": None,
                                "source_file": str(dest.relative_to(ROOT)).replace(
                                    "\\", "/"
                                ),
                                "source_url": None,
                                "confidence": 0.75,
                                "notes": "extracao automatica do zip archive.org (prova escrita)",
                            }
                        )
        if recs:
            vistos, unicos = set(), []
            for r in recs:
                k = (r["discipline"], r["question_number"], r["question_text"][:60])
                if k not in vistos:
                    vistos.add(k)
                    unicos.append(r)
            recs = unicos
        out = folder / f"discursivas_zip_{y}.jsonl"
        with out.open("w", encoding="utf-8") as fh:
            for r in recs:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"[ok] {out.name}: {len(recs)} registros")


if __name__ == "__main__":
    main()
