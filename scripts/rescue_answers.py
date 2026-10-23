"""Resgata respostas (gabarito) das rules antigas (versao HEAD do parquet)
e preenche os registros manuais correspondentes."""

import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/processed/questions.parquet"


def num(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


df = pd.read_parquet(PATH)
# parquet do HEAD (versao com as rules e gabaritos antes da limpeza)
blob = subprocess.run(
    ["git", "show", "HEAD:data/processed/questions.parquet"],
    cwd=ROOT,
    capture_output=True,
    check=True,
).stdout
tmp = Path(tempfile.gettempdir()) / "questions_head.parquet"
tmp.write_bytes(blob)
head = pd.read_parquet(tmp)
print(f"parquet HEAD: {len(head)} registros")

rules = head[
    head["extraction_method"].eq("rules")
    & head["stage"].eq("primeira_fase")
    & head["answer"].notna()
    & head["source_file"].str.contains("prova_objetiva", na=False)
]
print(f"rules de 1aF com resposta no HEAD: {len(rules)}")

filled = 0
for _, r in rules.iterrows():
    k_contest = r["contest_id"]
    k_qn = num(r["question_number"])
    k_itn = num(r["item_number"])
    m = df[
        df["extraction_method"].eq("manual")
        & (df["contest_id"] == k_contest)
        & df["question_number"].apply(num).eq(k_qn).fillna(False)
        & df["item_number"].apply(num).eq(k_itn).fillna(True)
    ]
    for i in m.index:
        if pd.isna(df.at[i, "answer"]):
            df.at[i, "answer"] = r["answer"]
            filled += 1

print(f"respostas resgatadas para os manuais: {filled}")
df.to_parquet(PATH, index=False)
print("parquet atualizado")
