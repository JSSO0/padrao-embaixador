"""M1.6 (D1): lista os itens da 1a fase sem resposta e sem note, por ano, e
cruza com os PDFs de gabarito disponiveis em data/raw."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data" / "processed" / "questions.parquet")
g = json_load = None
import json

g = json.loads(
    (ROOT / "data" / "processed" / "gabaritos.json").read_text(encoding="utf-8")
)


def num(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


m = df.stage.eq("primeira_fase")
sem = df[m & df.answer.isna() & ~df.notes.fillna("").str.contains("anulado")]
print(f"1a fase sem resposta e sem note: {len(sem)}")
print(sem.groupby("year").size().to_string())
print()
for y in sorted(sem.year.unique()):
    yg = g.get(str(y)) or {}
    qns = sorted({num(r["question_number"]) for _, r in sem[sem.year.eq(y)].iterrows()})
    folder = ROOT / "data" / "raw" / f"CACD_{y}"
    pdfs = [p.name for p in folder.rglob("gabarito*.pdf")] if folder.exists() else []
    print(
        f"{y}: {len(sem[sem.year.eq(y)])} itens | qns {qns[:6]}... | chaves no cache: {len(yg)} | pdfs: {pdfs}"
    )
