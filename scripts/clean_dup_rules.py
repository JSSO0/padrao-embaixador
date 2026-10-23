"""Remove do parquet as regras antigas (incompletas) de provas objetivas que
foram substituidas por transcries manuais.

Criterio seguro: mantem TODAS as rules de discursivas/segunda fase; remove
apenas rules de 'primeira_fase' cujo source_file e uma prova objetiva E cuja
(question_number, item_number) ja existe num registro manual do mesmo ano.

Uso: python scripts/clean_dup_rules.py [--dry-run]
"""

import argparse

import pandas as pd

PATH = "data/processed/questions.parquet"

df = pd.read_parquet(PATH)


def num(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


manual_keys = set()
m = df[df.extraction_method.eq("manual") & df.stage.eq("primeira_fase")]
for _, row in m.iterrows():
    manual_keys.add((row["contest_id"], num(row["question_number"])))

mask_dup = (
    df["extraction_method"].eq("rules")
    & df["stage"].eq("primeira_fase")
    & (df["source_file"].str.contains("prova_objetiva", na=False))
)
sub = df[mask_dup]
mask_dup = mask_dup & sub.apply(
    lambda r: (r["contest_id"], num(r["question_number"])) in manual_keys,
    axis=1,
).reindex(df.index, fill_value=False)

print(
    f"rules de prova objetiva substituidas por manual (mesma questao): {mask_dup.sum()}"
)
print(df[mask_dup].groupby("contest_id").size().to_string())

ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()
if args.dry_run:
    print("dry-run: nada escrito")
    raise SystemExit(0)

# transfere a resposta das rules removidas para os manuais correspondentes
# (o manual nasce com answer=null; a rule antiga tinha o gabarito)
idx_dup = df[mask_dup].index
moves = 0
for _, r in df.loc[idx_dup].iterrows():
    k = (r["contest_id"], num(r["question_number"]), num(r["item_number"]))
    if pd.isna(r["answer"]) or not str(r["answer"]).strip():
        continue
    cand = df.index[
        df["extraction_method"].eq("manual")
        & (df["contest_id"] == r["contest_id"])
        & df["question_number"].apply(num).eq(num(r["question_number"])).fillna(False)
        & df["item_number"].apply(num).eq(num(r["item_number"])).fillna(True)
    ]
    for i in cand:
        if pd.isna(df.at[i, "answer"]):
            df.at[i, "answer"] = r["answer"]
            moves += 1
print(f"respostas transferidas das rules para os manuais: {moves}")

df2 = df[~mask_dup].reset_index(drop=True)
df2.to_parquet(PATH, index=False)
print(f"parquet: {len(df)} -> {len(df2)}")
