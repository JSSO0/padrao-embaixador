"""Diff do snapshot B1 vs parquet atual (M1.3) + aceite de 2014."""

from pathlib import Path

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
novo["question_number"] = novo["question_number"].astype("Float64")
novo["item_number"] = novo["item_number"].astype("Int64")
novo = novo.sort_values(["contest_id", "stage", "question_number", "item_number"])
ant = pd.read_csv(
    SNAP, dtype={"answer": "string", "notes": "string", "topic": "string"}
)

key = ["contest_id", "stage", "question_number", "item_number"]
a = ant.set_index(key)
n = novo.set_index(key)
so_novo = n.index.difference(a.index)
so_antigo = a.index.difference(n.index)
comum = a.index.intersection(n.index)
print(
    f"linhas: antes={len(a)} depois={len(n)} | novas={len(so_novo)} sumidas={len(so_antigo)}"
)


def tag(ix):
    return sorted({(str(i[0]), str(i[1])) for i in ix})


print("novas por (contest,stage):", tag(so_novo))
print("sumidas por (contest,stage):", tag(so_antigo))

# diffs de campo fora de 2014 q32-73 (merge por chave; chaves duplicadas de
# 2004 (itn=qn) cruzam consigo mesmas com valores iguais — sem falso positivo)
cols = ["answer", "notes", "topic", "extraction_method", "discipline"]
mm = (
    a[cols]
    .reset_index()
    .merge(n[cols].reset_index(), on=key, how="inner", suffixes=("_a", "_n"))
)
print(f"pares comparados: {len(mm)}")
for col in cols:
    x = mm[f"{col}_a"].fillna("").astype(str)
    y = mm[f"{col}_n"].fillna("").astype(str)
    d = x != y
    if d.any():
        ch = mm.loc[d, key + [f"{col}_a", f"{col}_n"]]
        fora_2014 = ch[
            ~(ch.contest_id.eq("CACD_2014") & ch.question_number.between(32, 73))
        ]
        print(f"{col}: {int(d.sum())} mudancas | fora de 2014 q32-73: {len(fora_2014)}")
        if len(fora_2014):
            print(fora_2014.head(10).to_string())

# aceite M1.3
d14 = df[df.stage.eq("primeira_fase") & df.year.eq(2014)]
g = d14.groupby("question_number")
ok = (
    g.size().eq(4).all()
    and g.extraction_method.nunique().eq(1).all()
    and d14.extraction_method.eq("manual").all()
)
print(f"\n2014: {g.ngroups} questoes | todas manual e 4 itens: {ok}")
print(
    "disciplinas 2014:",
    d14.groupby("question_number")
    .discipline.agg(lambda s: s.iloc[0])
    .value_counts()
    .to_dict(),
)
print(
    "2014 com resposta:",
    int(d14.answer.notna().sum()),
    "/",
    len(d14),
    "| anulados com note:",
    int(d14.notes.fillna("").str.contains("anulado").sum()),
)
