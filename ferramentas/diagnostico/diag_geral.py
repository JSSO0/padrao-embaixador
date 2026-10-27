"""Analisa os itens com topic='geral' para entender que temas cobrir."""

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
m = df[
    df.stage.eq("primeira_fase") & df.topic.eq("geral") & df.discipline_canon.notna()
]

for disc in sorted(m.discipline_canon.unique()):
    sub = m[m.discipline_canon.eq(disc)]
    if len(sub) < 5:
        continue
    print("=" * 15, disc, f"({len(sub)} itens 'geral')")
    # amostra de 6 enunciados variados
    for _, r in sub.sample(min(6, len(sub)), random_state=42).iterrows():
        qt = str(r.question_text)[:130]
        print(f"   y{int(r.year)}: {qt!r}")
    print()
