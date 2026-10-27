"""Snapshot completo do questions.parquet para diff (B1/M1.3)."""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PARQUET = ROOT / "data" / "processed" / "questions.parquet"
SNAP = Path(__file__).with_suffix(".csv")

df = pd.read_parquet(PARQUET)
keep = [
    "contest_id",
    "stage",
    "question_number",
    "item_number",
    "discipline",
    "answer",
    "notes",
    "topic",
    "extraction_method",
    "source_file",
]
out = df[keep].copy()
out["question_number"] = out["question_number"].astype("Float64")
out["item_number"] = out["item_number"].astype("Int64")
out = out.sort_values(["contest_id", "stage", "question_number", "item_number"])
out.to_csv(SNAP, index=False)
print(f"snapshot: {len(out)} linhas -> {SNAP}")
