"""Diff multiset (linhas completas) entre snapshot B1 e parquet atual."""

from pathlib import Path
from collections import Counter

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SNAP = Path(__file__).with_name("snapshot_b1.csv")
df = pd.read_parquet(ROOT / "data" / "processed" / "questions.parquet")

keep = [
    "contest_id",
    "stage",
    "question_number",
    "item_number",
    "discipline",
    "answer",
    "notes",
    "topic",
    "extraction_method",
    "source_file",
]
novo = df[keep].copy()
novo["question_number"] = novo["question_number"].astype("Float64").astype(str)
novo["item_number"] = novo["item_number"].astype("Int64").astype(str)
novo = novo.replace({"item_number": {"<NA>": ""}, "question_number": {"<NA>": ""}})
novo = novo.fillna("").astype(str)
ant = pd.read_csv(SNAP, dtype=str, keep_default_na=False)[keep]
# normaliza item_number 'nan'/'<NA>' -> ''
for d in (ant, novo):
    d["item_number"] = d["item_number"].replace({"<NA>": "", "nan": ""}, regex=False)

ca, cn = (
    Counter(map(tuple, ant.itertuples(index=False, name=None))),
    Counter(map(tuple, novo.itertuples(index=False, name=None))),
)
so_novo = cn - ca  # conteudos que apareceram
so_antigo = ca - cn  # conteudos que sumiram
print(f"apareceram: {sum(so_novo.values())} | sumiram: {sum(so_antigo.values())}")


def resumo(counter, n=200):
    por = Counter()
    for row in counter.elements():
        por[(row[0], row[1])] += 1
    return dict(por)


print("apareceram por (contest,stage):", resumo(so_novo))
print("sumiram por (contest,stage):", resumo(so_antigo))

# pares (sumiu, apareceu) para ver mudancas reais fora de 2014 q32-73
lost = list(so_antigo.elements())
got = list(so_novo.elements())
fora = [
    r
    for r in got
    if not (r[0] == "CACD_2014" and r[1] == "primeira_fase" and 32 <= float(r[2]) <= 73)
]
fora_l = [r for r in lost] if (lost := list(so_antigo.elements())) else []
fora_l = [
    r
    for r in fora_l
    if not (r[0] == "CACD_2014" and r[1] == "primeira_fase" and 32 <= float(r[2]) <= 73)
]
print(f"\nfora de 2014 q32-73: apareceram={len(fora)} sumiram={len(fora_l)}")
for r in fora_l[:20]:
    print(
        "  SUMIU:",
        r[0],
        r[1],
        "q",
        r[2],
        "it",
        r[3],
        "|",
        r[8],
        "| ans=",
        r[5],
        "| topic=",
        r[7],
    )
for r in fora[:20]:
    print(
        "  ENTROU:",
        r[0],
        r[1],
        "q",
        r[2],
        "it",
        r[3],
        "|",
        r[8],
        "| ans=",
        r[5],
        "| topic=",
        r[7],
    )
