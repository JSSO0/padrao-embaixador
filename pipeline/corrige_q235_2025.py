# -*- coding: utf-8 -*-
"""Corrige as questoes 235-236 da 1a fase CACD 2025 (M1.7).

Defeito: o extrator linear perdeu o enunciado compartilhado das questoes 235 e
236 ("A Constituicao Federal de 1988 preve como principio que rege Republica
Federativa do Brasil em suas relacoes internacionais"), deixando q235 apenas
com o fragmento e q236 com o enunciado da questao seguinte colado.
Corrige o JSONL fonte e o parquet, com note de reconstrucao.
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
STEM = (
    "A Constituição Federal de 1988 prevê como princípio que rege "
    "República Federativa do Brasil em suas relações internacionais:"
)
ITENS = {
    235: " o repúdio ao terrorismo e ao racismo.",
    236: " a não concessão de extradição a estrangeiro por crime político ou de opinião.",
}
NOTE = "enunciado reconstruido do PDF (M1.7: q235-236 compartilham o enunciado)"

# 1) JSONL fonte
f = ROOT / "data/raw/CACD_2025/cebraspe/cacd_2025_primeira_fase_prova_objetiva_2.jsonl"
lines = f.read_text(encoding="utf-8").splitlines()
for i, l in enumerate(lines):
    o = json.loads(l)
    qn = o.get("question_number")
    if qn in ITENS:
        o["question_text"] = STEM + ITENS[qn]
        o["item_text"] = None
        o["notes"] = NOTE
        lines[i] = json.dumps(o, ensure_ascii=False)
        print(f"jsonl q{qn}: corrigido")
f.write_text("\n".join(lines) + "\n", encoding="utf-8")

# 2) parquet
pf = ROOT / "data/processed/questions.parquet"
df = pd.read_parquet(pf)
m = (
    df.stage.eq("primeira_fase")
    & df.year.eq(2025)
    & df.question_number.isin([235, 236])
)
for idx in df[m].index:
    qn = int(df.at[idx, "question_number"])
    df.at[idx, "question_text"] = STEM + ITENS[qn]
    df.at[idx, "notes"] = NOTE
    print(f"parquet q{qn}: corrigido")
df.to_parquet(pf, index=False)
print("ok")
