"""Overview do andamento das questes por ano: cobertura manual x rules,
primeira fase x segunda fase, gabaritos."""

import sys
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
df = pd.read_parquet(ROOT / "data/processed/questions.parquet")

LINHA = "-" * 96
print("OVERVIEW QUESTOES CACD 2003-2026  (data/processed/questions.parquet)")
print(LINHA)

for contest in sorted(df.contest_id.unique()):
    d = df[df.contest_id == contest]
    fase1 = d[d.stage == "primeira_fase"]
    manual = fase1[fase1.extraction_method == "manual"]
    rules = fase1[fase1.extraction_method == "rules"]
    disc = d[d.stage != "primeira_fase"]

    qm = set(manual.question_number.dropna().astype(int))
    qr = set(rules.question_number.dropna().astype(int))
    uniao = sorted(qm | qr)
    faixa = f"{uniao[0]}-{uniao[-1]}" if uniao else "-"
    # lacunas na uniao
    lacunas = []
    if uniao:
        prev = uniao[0]
        for q in uniao[1:]:
            if q > prev + 1:
                lacunas.append(f"{prev + 1}-{q - 1}")
            prev = q

    ans = d.answer.notna().mean() if len(d) else 0

    print(f"\n{contest}")
    print(
        f"  1a fase: {len(fase1):4} itens | {len(qm | qr):3} questoes | faixa {faixa}"
        + (f" | lacunas: {', '.join(lacunas)}" if lacunas else " | sem lacunas")
    )
    if len(manual):
        print(
            f"    manual: {len(manual):4} itens ({len(qm):3} q)  |  "
            f"rules: {len(rules):3} itens ({len(qr - qm):3} q nao cobertas pelo manual)"
        )
    else:
        print(f"    rules: {len(rules):3} itens (sem manual)")
    if len(disc):
        print(
            f"  2a fase (discursivas): {len(disc):4} itens | "
            f"{disc.question_number.nunique():3} questoes"
        )
    print(
        f"  gabarito preenchido: {ans:5.1%} | fontes: {dict(d.source_type.value_counts())}"
    )
