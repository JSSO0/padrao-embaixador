# -*- coding: utf-8 -*-
"""Corrige o item 3 da questao 13 de 2013 (unico problema da amostra M1.9).

A transcricao diz "por ter sido estrangulada e entrar"; o PDF da prova diz
"por ser estrangulada e entrar". Item de gramatica: a troca muda o que se
julga. Corrige o JSONL fonte e o parquet.
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ANTES = "fossem substituídas, respectivamente, por ter sido estrangulada e"
DEPOIS = "fossem substituídas, respectivamente, por ser estrangulada e"

# 1) JSONL fonte
f = ROOT / "data/raw/CACD_2013/cursocacd/cacd_2013_primeira_fase_prova_objetiva_1.jsonl"
lines = f.read_text(encoding="utf-8").splitlines()
fix = 0
for i, l in enumerate(lines):
    o = json.loads(l)
    if o.get("question_number") == 13 and o.get("item_number") == 3:
        it = o.get("item_text") or ""
        if ANTES in it:
            o["item_text"] = it.replace(ANTES, DEPOIS)
            lines[i] = json.dumps(o, ensure_ascii=False)
            fix += 1
if fix:
    f.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"jsonl: {fix} linha(s) corrigida(s)")

# 2) parquet
pf = ROOT / "data/processed/questions.parquet"
df = pd.read_parquet(pf)
m = (
    df.stage.eq("primeira_fase")
    & df.year.eq(2013)
    & df.question_number.eq(13)
    & df.item_number.eq(3)
)
for idx in df[m].index:
    it = str(df.at[idx, "item_text"])
    if ANTES in it:
        df.at[idx, "item_text"] = it.replace(ANTES, DEPOIS)
        print("parquet: item 13/3 corrigido")
df.to_parquet(PATH := pf, index=False)
print("ok")
