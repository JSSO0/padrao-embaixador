"""Snapshot de seguranca para A1 (M1.1): salva respostas de 2003-2014
(1a fase) em CSV e resume o cache de gabaritos. Uso:
    python ferramentas/diagnostico/snapshot_a1.py salvar|comparar
"""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PARQUET = ROOT / "data" / "processed" / "questions.parquet"
CACHE = ROOT / "data" / "processed" / "gabaritos.json"
SNAP = Path(__file__).with_suffix(".csv")

COLS = ["contest_id", "year", "question_number", "item_number", "answer", "notes"]


def subset(df: pd.DataFrame) -> pd.DataFrame:
    m = df.stage.eq("primeira_fase") & df.year.between(2003, 2014)
    # CACD_2003 tem year=2004 nas linhas; entra por contest_id
    m |= df.contest_id.eq("CACD_2003")
    out = df[m][COLS].copy()
    out["question_number"] = out["question_number"].astype("Float64")
    out["item_number"] = out["item_number"].astype("Int64")
    return out.sort_values(
        ["contest_id", "question_number", "item_number"]
    ).reset_index(drop=True)


mode = sys.argv[1] if len(sys.argv) > 1 else "salvar"
df = pd.read_parquet(PARQUET)
sub = subset(df)
if mode == "salvar":
    sub.to_csv(SNAP, index=False)
    print(f"snapshot salvo: {SNAP} ({len(sub)} linhas 2003-2014)")
    import json

    g = json.loads(CACHE.read_text(encoding="utf-8"))
    for y in sorted(g):
        print(f"  cache {y}: {len(g[y])} respostas")
else:
    ant = pd.read_csv(SNAP, dtype={"answer": "string", "notes": "string"})
    novo = sub.copy()
    for c in ("answer", "notes"):
        ant[c] = ant[c].fillna("")
        novo[c] = novo[c].fillna("")
    ant["item_number"] = ant["item_number"].fillna(-1).astype(int)
    novo["item_number"] = novo["item_number"].fillna(-1).astype(int)
    novo["question_number"] = novo["question_number"].astype(int)
    ant["question_number"] = ant["question_number"].astype(int)
    key = ["contest_id", "year", "question_number", "item_number"]
    a = ant.set_index(key)
    n = novo.set_index(key)
    apenas_novo = n.index.difference(a.index)
    apenas_antigo = a.index.difference(n.index)
    comum = a.index.intersection(n.index)
    diff_ans = (
        a.loc[comum, "answer"].fillna("") != n.loc[comum, "answer"].fillna("")
    ).sum()
    diff_notes = (
        a.loc[comum, "notes"].fillna("") != n.loc[comum, "notes"].fillna("")
    ).sum()
    print(f"linhas 2003-2014: antes={len(a)} depois={len(n)}")
    print(f"somente depois={len(apenas_novo)} somente antes={len(apenas_antigo)}")
    print(f"answer alterada: {diff_ans} | notes alterada: {diff_notes}")
    if len(apenas_novo):
        print("novas linhas:", list(apenas_novo)[:10])
    if len(apenas_antigo):
        print("linhas sumidas:", list(apenas_antigo)[:10])
    if diff_ans:
        d = a.loc[comum]
        ch = d[d["answer"].fillna("") != n.loc[comum, "answer"].fillna("")]
        print(ch[["answer"]].head(15).to_string())
