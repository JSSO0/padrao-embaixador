"""Detalha os itens 1a fase sem resposta e sem note (M1.6)."""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data" / "processed" / "questions.parquet")
g = json.loads(
    (ROOT / "data" / "processed" / "gabaritos.json").read_text(encoding="utf-8")
)


def num(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


sem = df[
    df.stage.eq("primeira_fase")
    & df.answer.isna()
    & ~df.notes.fillna("").str.contains("anulado")
]
for _, r in sem.sort_values(["year", "question_number", "item_number"]).iterrows():
    y = str(int(r["year"]))
    qn = num(r["question_number"])
    itn = num(r["item_number"])
    yg = g.get(y) or {}
    chaves_qn = sorted(k for k in yg if k.split(":")[0] == str(qn))
    letra = None
    if qn is not None:
        letra = (
            yg.get(f"{qn}:{itn}")
            if itn is not None
            else (yg.get(f"{qn}:0") or yg.get(f"{qn}:1"))
        )
    print(
        f"{r['contest_id']} q{qn} it{itn} [{r['extraction_method']}] | "
        f"chaves gabarito p/ qn: {chaves_qn if chaves_qn else 'NENHUMA'} | letra=?"
    )
