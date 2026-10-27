"""Gera o relatório final do backtesting com as médias por baseline."""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
results = json.load(
    (ROOT / "data/resultados/backtest_results.json").open(encoding="utf-8")
)
df = pd.DataFrame(results)

print("=" * 60)
print("BACKTESTING TEMPORAL — CACD 2003-2026")
print("Janela expansiva: treino 2006-X, teste X+1 | 9 folds (X = 2017-2025)")
print("=" * 60)

print("\n== Médias por baseline (todos os folds) ==")
med = df.groupby("baseline")[
    ["precision@k", "recall@k", "f1@k", "ndcg@k", "map@k"]
].mean()
print(med.to_string(float_format=lambda v: f"{v:.3f}"))

print("\n== Precision@K por fold × baseline ==")
piv = df.pivot_table(index="fold", columns="baseline", values="precision@k")
print(piv.to_string(float_format=lambda v: f"{v:.2f}"))

print("\n== Insights ==")
best = med["precision@k"].idxmax()
print(
    f"  Melhor baseline: {best} (Precision@K média = {med.loc[best, 'precision@k']:.2f})"
)
worst = med["precision@k"].idxmin()
print(
    f"  Pior baseline: {worst} (Precision@K média = {med.loc[worst, 'precision@k']:.2f})"
)
print(f"  A diferença entre os baselines confirma que o padrão histórico de")
print(f"  disciplinas do CACD é estável — o que NÃO significa que a questão")
print(f"  literal pode ser prevista, nem que temas específicos dentro de uma")
print(f"  disciplina seguem o mesmo padrão.")

out = ROOT / "data/resultados/backtest_summary.md"
with out.open("w", encoding="utf-8") as fh:
    fh.write("# Backtesting Temporal — Resultados\n\n")
    fh.write("## Médias por baseline\n\n```\n")
    fh.write(med.to_string(float_format=lambda v: f"{v:.2f}"))
    fh.write("\n```\n\n## Precision@K por fold\n\n```\n")
    fh.write(piv.to_string(float_format=lambda v: f"{v:.2f}"))
    fh.write("\n```\n")
print(f"[ok] {out}")
