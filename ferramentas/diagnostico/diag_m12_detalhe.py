"""Detalhe das 80 linhas de 1a fase vindas de discursiva (M1.2)."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data" / "processed" / "questions.parquet")

m = df.stage.eq("primeira_fase") & df.source_file.fillna("").str.contains(
    "discursiva", case=False, regex=False
)
sub = df[m]
print(sub.groupby("discipline", dropna=False).size().to_string())
print("\ncom resposta, por ano/disciplina:")
cr = sub[sub.answer.notna()]
print(cr.groupby(["year", "discipline"]).size().to_string())
print("\namostra com resposta:")
print(
    cr[["year", "question_number", "discipline", "answer", "question_type"]]
    .head(20)
    .to_string()
)
print("\nquestion_type:", sub.question_type.value_counts(dropna=False).to_dict())
print("topic nulo:", int(sub.topic.isna().sum()), "/", len(sub))
# ha alguma questao de 1a fase REAL (objetiva) que dependa dessas linhas?
print(
    "\nlinhas de discursiva com answer e sem par manual de 1a fase no mesmo (contest, qn):",
)
for _, r in cr.iterrows():
    qn = r["question_number"]
    has_manual = (
        (df.extraction_method.eq("manual"))
        & (df.stage.eq("primeira_fase"))
        & (df.contest_id == r["contest_id"])
        & df.question_number.apply(lambda v: v == qn if pd.notna(v) else False)
    ).any()
    if not has_manual:
        print(
            f"  sem manual: {r['contest_id']} q{qn} ({r['discipline']}) ans={r['answer']}"
        )
