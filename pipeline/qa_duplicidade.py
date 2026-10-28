"""Teste de duplicidade do parquet (M1.8/E1).

Chave de unicidade: contest_id + stage + discipline + question_number + item_number.
Aceite: duplicated().sum() == 0.
Uso: python pipeline/qa_duplicidade.py [--dry-run]
"""

import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
KEY = ["contest_id", "stage", "discipline", "question_number", "item_number"]

df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
d = df[KEY].copy()
d["question_number"] = d["question_number"].astype("Float64")
d["item_number"] = d["item_number"].astype("Int64")
d = d.fillna({"discipline": "", "question_number": -1, "item_number": -1})

dups = d.duplicated(keep=False)
n = int(dups.sum())
print(f"duplicadas (contest+stage+discipline+qn+itn): {n}")
if n:
    sub = df.loc[d[dups].index]
    g = sub.groupby(KEY[:2], dropna=False).size()
    print(g.to_string())
    print("\ndetalhe (ate 40):")
    print(sub[KEY].head(40).to_string())
print("ACEITE M1.8:", "PASS" if n == 0 else f"FAIL ({n} duplicatas)")
