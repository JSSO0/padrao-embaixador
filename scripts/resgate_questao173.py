"""Recupera o texto integral das 'questoes' ruidas de 2013 (removidas em 6664abf)."""

import subprocess
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
raw = subprocess.run(
    ["git", "show", "6664abf~1:data/processed/questions.parquet"],
    capture_output=True,
).stdout
tmp = ROOT / "_tmp_prev.parquet"
tmp.write_bytes(raw)

df = pd.read_parquet(tmp)
tmp.unlink()
m13 = df[
    df.contest_id.eq("CACD_2013")
    & df.stage.eq("primeira_fase")
    & df.extraction_method.eq("rules")
]
qn = pd.to_numeric(m13.question_number, errors="coerce")
noise = m13[(qn > 73).fillna(False)].sort_values("question_number")

r = noise.iloc[0]
print(f"=== A 'QUESTÃO {int(r.question_number)}' na íntegra ===")
print(str(r.question_text)[:700])
print()
print("=== e a 'QUESTÃO 228' (a última) ===")
r2 = noise.iloc[-1]
print(str(r2.question_text)[:400])
