"""Inspeciona os 5 defeitos pontuais do M1.7."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data" / "processed" / "questions.parquet")
pf = df[df.stage.eq("primeira_fase")]

print("== 2004: linhas achatadas itn=qn ==")
d = pf[pf.year.eq(2004)]
flat = d[d.item_number.eq(d.question_number)]
print(
    f"total={len(d)} | achatadas (itn=qn)={len(flat)} | qns: {sorted(flat.question_number.unique())[:8]}..."
)
r = flat.iloc[0]
print(
    "exemplo: q",
    r.question_number,
    "itn",
    r.item_number,
    "| texto:",
    str(r.item_text)[:80],
)
g = d[d.contest_id.eq("CACD_2004")]
print(
    "por qn: n linhas ->", d.groupby("question_number").size().value_counts().to_dict()
)

print("\n== 2013 qn 174-227 ==")
d13 = pf[pf.year.eq(2013)]
print(
    "presentes:",
    int(d13.question_number.between(174, 227).sum()),
    "| qns 2013:",
    sorted(d13.question_number.unique())[:5],
    "...",
    sorted(d13.question_number.unique())[-3:],
)

print("\n== 2025 qn 235 ==")
d25 = pf[pf.year.eq(2025)]
qns25 = sorted(d25.question_number.dropna().unique())
print(
    "2025: qns",
    qns25[0],
    "-",
    qns25[-1],
    "| count qns:",
    len(qns25),
    "| faltam:",
    [q for q in range(1, 241) if q not in qns25],
)

print("\n== 2018 q40 ==")
r = pf[(pf.year.eq(2018)) & (pf.question_number.eq(40))]
for _, row in r.head(1).iterrows():
    print("question_text (fim):", repr(str(row.question_text)[-120:]))

print("\n== 2024: questoes com texto-base suspeito ==")
d24 = pf[pf.year.eq(2024)]
# textos-base: questoes cujo question_text menciona "Text" ou LI em disciplina errada
sus = d24[d24.question_text.fillna("").str.contains("Text", regex=False)]
print(
    "qns com 'Text' no enunciado:",
    sorted(sus.question_number.dropna().unique().tolist())[:40],
)
