# -*- coding: utf-8 -*-
"""Verifica conteudo de questoes 2024 sinalizadas pela auditoria (v2)."""

import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
for qn in (9, 10, 20, 47, 48, 58):
    d = df[
        (df.stage == "primeira_fase")
        & (df.contest_id.eq("CACD_2024"))
        & (df.question_number.eq(qn))
    ]
    r = d.iloc[0]
    print(f"2024 q{qn} [{r.discipline_canon}]:", repr(str(r.question_text)[:115]))
    print()
