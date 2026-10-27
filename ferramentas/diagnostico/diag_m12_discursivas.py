"""Inspeciona linhas de 1a fase vindas de PDFs de discursiva (M1.2)."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data" / "processed" / "questions.parquet")

m = df.stage.eq("primeira_fase") & df.source_file.fillna("").str.contains(
    "discursiva", case=False, regex=False
)
print(f"total parquet: {len(df)} | 1a fase com source_file discursiva*: {m.sum()}")
print(df[m].groupby(["year", "extraction_method"]).size().to_string())
print("\nsource_file distintos:")
print(df[m].source_file.value_counts().to_string())
print("\namostra (ate 15):")
cols = [
    "contest_id",
    "stage",
    "question_number",
    "item_number",
    "discipline",
    "answer",
    "extraction_method",
    "source_file",
]
print(df[m][cols].head(15).to_string())
print("\ncom resposta preenchida:", int(df[m].answer.notna().sum()))
