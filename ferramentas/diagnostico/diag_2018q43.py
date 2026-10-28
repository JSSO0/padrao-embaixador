# -*- coding: utf-8 -*-
"""Debug do item 2018 q43/1: hits por tema."""

import sys
from pathlib import Path

import pandas as pd
import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
tax = yaml.safe_load(
    (ROOT / "data/metadata/taxonomia.yaml").read_text(encoding="utf-8")
)["taxonomia"]
df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
r = df[
    (df.stage == "primeira_fase")
    & (df.contest_id.eq("CACD_2018"))
    & (df.question_number.eq(43))
    & (df.item_number.eq(1))
].iloc[0]
texto = (str(r["question_text"]) + " " + str(r["item_text"] or "")).lower()
print(repr(texto[:200]))
for tema, info in tax["disciplinas"]["Língua Inglesa"].items():
    hits = [kw for kw in info["keywords"] if kw.lower() in texto]
    if hits:
        print(f"{tema}: {len(hits)} -> {hits}")
