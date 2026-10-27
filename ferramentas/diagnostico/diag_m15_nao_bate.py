"""Das linhas com note='anulado', quais nao batem com chave X no gabarito?"""

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


m = df.stage.eq("primeira_fase") & df.notes.fillna("").str.contains("anulado")
for idx, row in df[m].iterrows():
    y = "2003" if str(row["contest_id"]) == "CACD_2003" else str(int(row["year"]))
    qn = num(row["question_number"])
    itn = num(row["item_number"])
    yg = g.get(y) or {}
    if itn is not None:
        letter = yg.get(f"{qn}:{itn}")
    else:
        letter = yg.get(f"{qn}:0") or yg.get(f"{qn}:1")
    if letter is None or str(letter).upper() not in ("X", "#", "☼"):
        print(
            f"NAO-BATE: {row['contest_id']} q{qn} it{itn} ans={row['answer']} "
            f"gab_key={letter} notes={row['notes']!r} "
            f"src={row['source_file']}"
        )
