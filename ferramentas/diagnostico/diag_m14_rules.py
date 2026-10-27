"""Inspeciona as linhas rules restantes da 1a fase (M1.4) e defeitos pontuais (M1.7)."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data" / "processed" / "questions.parquet")
m = df.stage.eq("primeira_fase") & df.extraction_method.eq("rules")
r = df[m]
print(f"rules na 1a fase: {len(r)}")
print(r.groupby(["year", "question_number"]).size().to_string())
print("\ndetalhe:")
for _, row in r.iterrows():
    print(
        f"  {row['contest_id']} q{row['question_number']} it{row['item_number']} "
        f"disc={row['discipline']} ans={row['answer']} src={str(row['source_file']).split('/')[-1][:50]}"
    )
# notes/justificativa existentes
print("\ncom notes:", int(r.notes.notna().sum()))

# defeitos pontuais (M1.7)
print("\n--- M1.7 defeitos pontuais ---")
d04 = df[df.stage.eq("primeira_fase") & df.year.eq(2004)]
print(
    "2004 linhas com itn=qn:",
    int((d14 := d04).item_number.eq(d04.question_number).sum()),
    "/",
    len(d04),
)
d13 = df[df.stage.eq("primeira_fase") & df.year.eq(2013)]
print("2013 qn 174-227:", int(d13.question_number.between(174, 227).sum()))
for y in (2024, 2025, 2018):
    d = df[df.stage.eq("primeira_fase") & df.year.eq(y)]
    print(f"{y}: {len(d)} linhas")
d25 = df[df.stage.eq("primeira_fase") & df.year.eq(2025)]
print(
    "2025 item 235 presente:",
    int(d25.item_number.eq(235).sum()) if len(d25) else 0,
    "| max itn:",
    int(d25.item_number.max()) if d25.item_number.notna().any() else None,
)
print(
    "2018 q40 linhas:",
    len(
        df[df.stage.eq("primeira_fase") & df.year.eq(2018) & df.question_number.eq(40)]
    ),
)
