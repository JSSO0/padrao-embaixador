"""Remove do parquet as linhas de 1a fase extraidas de PDFs de discursiva.

O parser segmentador, em algumas edicoes (2006/2007 cursocacd, 2015/2017/2023
cursocacd, 2024-2026 cebraspe), enxergou secoes de provas discursivas e criou
linhas com stage='primeira_fase' e source_file de discursiva — com "disciplinas"
como "Preguntas", "Rascunho", "Resumen", "(...)" e sem question_number. Sao lixo
de parser: nenhum item legitimo de 1a fase vem de PDF discursivo.

Criterio: stage == 'primeira_fase' E source_file contem 'discursiva'.

Uso: python pipeline/remove_discursivas_primeira_fase.py [--dry-run]
"""

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "processed" / "questions.parquet"

df = pd.read_parquet(PATH)

mask = df.stage.eq("primeira_fase") & df.source_file.fillna("").str.contains(
    "discursiva", case=False, regex=False
)

print(f"linhas de 1a fase vindas de PDF discursiva: {int(mask.sum())}")
print(df[mask].groupby("contest_id").size().to_string())

ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()
if args.dry_run:
    print("dry-run: nada escrito")
    raise SystemExit(0)

df2 = df[~mask].reset_index(drop=True)
df2.to_parquet(PATH, index=False)
print(f"parquet: {len(df)} -> {len(df2)}")

# verificacao do criterio de aceite (M1.2)
chk = pd.read_parquet(PATH)
rest = chk.stage.eq("primeira_fase") & chk.source_file.fillna("").str.contains(
    "discursiva", case=False, regex=False
)
print(f"verificacao: linhas de discursiva restantes na 1a fase = {int(rest.sum())}")
