# -*- coding: utf-8 -*-
"""Inspeciona as linhas Cultura Geral de 2004 (M2/B1)."""

import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
d = df[
    (df.stage == "primeira_fase")
    & (df.year == 2004)
    & df.discipline.eq("Cultura Geral")
]
for _, r in d.head(4).iterrows():
    print(f"q{r.question_number} it{r.item_number}:", repr(str(r.question_text)[:160]))
    print()
print("canon:", d.discipline_canon.unique().tolist())
