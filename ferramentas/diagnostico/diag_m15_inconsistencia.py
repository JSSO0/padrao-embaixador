"""Localiza linhas com notes='anulado' mas com resposta preenchida (M1.5)."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data" / "processed" / "questions.parquet")
m = df.notes.fillna("").str.contains("anulado", case=False)
sub = df[m]
print(
    f"total com note anulado: {len(sub)} | por stage: {sub.stage.value_counts().to_dict()}"
)
inv = sub[sub.answer.notna() & sub.answer.astype(str).str.strip().ne("")]
print(f"com resposta preenchida: {len(inv)}")
cols = [
    "contest_id",
    "stage",
    "question_number",
    "item_number",
    "answer",
    "notes",
    "extraction_method",
    "year",
]
print(inv[cols].to_string())
