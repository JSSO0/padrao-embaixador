"""Analisa os enunciados das 4.951 objetivas por disciplina para extrair
os temas recorrentes (para desenhar a taxonomia)."""

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
m = df[
    df.stage.eq("primeira_fase")
    & df.discipline_canon.notna()
    & df.discipline_canon.ne("Preguntas")
    & df.discipline_canon.ne("Rascunho")
    & df.discipline_canon.ne("Admissão À Carreira De Diplomata")
    & df.discipline_canon.ne("Cultura Geral")
    & df.discipline_canon.ne("Resumen")
    & df.discipline_canon.ne("Textual Exercises")
    & df.discipline_canon.ne("Ong")
    & df.discipline_canon.ne("Realização")
]

for disc in sorted(m.discipline_canon.unique()):
    sub = m[m.discipline_canon.eq(disc)]
    print(
        "=" * 25, disc, f"({len(sub)} itens, {sub.question_number.nunique()} questoes)"
    )
    for year in sorted(sub.year.unique())[:6]:
        r = sub[sub.year.eq(year)].iloc[0]
        qt = str(r.question_text)[:120]
        print(f"   {int(r.year)}: {qt!r}")
    print()
