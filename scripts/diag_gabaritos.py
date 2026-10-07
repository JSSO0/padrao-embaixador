# -*- coding: utf-8 -*-
"""Diagnostico de gabaritos: cobertura por edicao e pares por arquivo."""

import pandas as pd

q = pd.read_parquet("data/processed/questions.parquet")
cov = q.groupby("contest_id").agg(
    n=("question_id", "count"), com_gab=("answer", lambda s: s.notna().mean())
)
print("=== cobertura de gabarito por edicao ===")
for c, row in cov.iterrows():
    flag = "OK" if row.com_gab > 0.8 else ("PARCIAL" if row.com_gab > 0 else "ZERO")
    print(f"{c}: {int(row.n)} itens | gabarito {row.com_gab:.0%} | {flag}")

r = pd.read_csv("data/processed/extraction_report.csv")
g = r[r["doc_role"] == "gabarito"][["source_file", "questions_found"]]
print()
print("=== gabaritos parseados (pares por arquivo) ===")
for _, row in g.iterrows():
    nome = str(row["source_file"]).split("raw/")[1]
    print(f"{nome[:64]:64s} -> {row['questions_found']} pares")
