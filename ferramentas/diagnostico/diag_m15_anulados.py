"""Inspeciona anulados na 1a fase (M1.5): itens cujo gabarito oficial e X/#/☼."""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data" / "processed" / "questions.parquet")
g = json.loads(
    (ROOT / "data" / "processed" / "gabaritos.json").read_text(encoding="utf-8")
)

m = df.stage.eq("primeira_fase") & df.extraction_method.isin(["manual", "rules"])
print("notes existentes (1a fase manual+rules):")
print(df[m].notes.fillna("(vazio)").value_counts().head(15).to_string())


def num(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


stats = {
    "anulado_com_note": 0,
    "anulado_sem_note": 0,
    "sem_gabarito": 0,
    "com_resposta": 0,
}
sem_note = []
for idx, row in df[m].iterrows():
    contest = str(row["contest_id"])
    y = "2003" if contest == "CACD_2003" else str(int(row["year"]))
    qn = num(row["question_number"])
    itn = num(row["item_number"])
    ans = row["answer"]
    has_ans = pd.notna(ans) and bool(str(ans).strip())
    if has_ans:
        stats["com_resposta"] += 1
        continue
    letter = None
    yg = g.get(y) or {}
    if qn is not None:
        if itn is not None:
            letter = yg.get(f"{qn}:{itn}")
        else:
            letter = yg.get(f"{qn}:0") or yg.get(f"{qn}:1")
    if letter is None:
        stats["sem_gabarito"] += 1
        continue
    if str(letter).upper() in ("X", "#", "☼"):
        note = row["notes"]
        if pd.notna(note) and "anulado" in str(note).lower():
            stats["anulado_com_note"] += 1
        else:
            stats["anulado_sem_note"] += 1
            sem_note.append((contest, qn, itn, str(note)))

print("\nsem resposta na 1a fase:")
for k, v in stats.items():
    print(f"  {k}: {v}")
print("\nanulados sem note (ate 30):")
for t in sem_note[:30]:
    print(" ", t)
