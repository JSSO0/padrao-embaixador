"""Estado da transricao 2014 na 1a fase (M1.3)."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data" / "processed" / "questions.parquet")
d = df[df.stage.eq("primeira_fase") & df.year.eq(2014)].copy()

print(f"2014 1a fase: {len(d)} linhas")
print("\npor questao (n itens / metodo / tem resposta):")
for qn, g in d.groupby("question_number"):
    ans = g.answer.notna().sum()
    met = ",".join(sorted(g.extraction_method.unique()))
    src = g.source_file.iloc[0].split("/")[-1][:45]
    print(
        f"  q{int(qn):3d}: {len(g)} itens | {met:6s} | resp={int(g.answer.notna().sum())}"
        f" | disc={g.discipline.iloc[0] if pd.notna(g.discipline.iloc[0]) else '-'} | {src}"
    )
