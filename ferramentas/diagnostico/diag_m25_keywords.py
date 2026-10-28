# -*- coding: utf-8 -*-
"""Diagnostico dos 18 erros da validacao M2.5: keywords que casaram."""

import re
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

CASOS = [
    ("CACD_2011", 61, 1, "comércio_internacional"),
    ("CACD_2004", 91, 91, "urbanização"),
    ("CACD_2003", 25, 5, "internacional_público"),
    ("CACD_2026", 115, None, "meio_ambiente"),
    ("CACD_2017", 68, 3, "desenvolvimento"),
    ("CACD_2026", 121, None, "reading_comprehension"),
    ("CACD_2006", 14, 1, "gramática"),
    ("CACD_2013", 7, 4, "semântica"),
    ("CACD_2003", 30, 2, "desenvolvimento"),
    ("CACD_2003", 4, 1, "semântica"),
    ("CACD_2026", 201, None, "macroeconomia"),
    ("CACD_2018", 43, 1, "vocabulary"),
    ("CACD_2017", 55, 4, "revoluções_liberais"),
    ("CACD_2024", 55, 1, "revoluções_liberais"),
    ("CACD_2012", 27, 3, "urbanização"),
    ("CACD_2024", 39, 2, "reading_comprehension"),
    ("CACD_2015", 52, 3, "revoluções_liberais"),
]

for contest, qn, itn, correto in CASOS:
    sub = df[
        (df.stage == "primeira_fase")
        & (df.contest_id.eq(contest))
        & (df.question_number.eq(qn))
    ]
    r = sub.iloc[0] if itn is None else sub[sub.item_number.eq(itn)].iloc[0]
    disc = r["discipline_canon"]
    texto = (str(r["question_text"]) + " " + str(r["item_text"] or "")).lower()
    print(
        f"=== {contest} Q{qn}/{itn} ({disc}) atribuido={r['topic']} | correto={correto}"
    )
    print("   texto:", repr(texto[:140]))
    scores = []
    for tema, info in tax["disciplinas"][disc].items():
        hits = [kw for kw in info["keywords"] if kw.lower() in texto]
        if hits:
            scores.append((len(hits), tema, hits[:4]))
    for s, tema, hits in sorted(scores, reverse=True)[:4]:
        print(f"    {s} hits: {tema} {hits}")
    print()
