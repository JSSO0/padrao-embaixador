"""Analisa os itens com topic='geral' por disciplina para identificar os temas ausentes."""

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
m = df[
    df.stage.eq("primeira_fase") & df.topic.eq("geral") & df.discipline_canon.notna()
]

for disc in sorted(m.discipline_canon.unique()):
    sub = m[m.discipline_canon.eq(disc)]
    if len(sub) < 5:
        continue
    print("=" * 20, disc, f"({len(sub)} itens 'geral')")
    # amostra com o texto combinado (enunciado + item)
    for _, r in sub.sample(min(8, len(sub)), random_state=7).iterrows():
        qt = (str(r.question_text) + " " + str(r.item_text or ""))[:150]
        print(f"   y{int(r.year)}: {qt!r}")
    print()
