"""Gráfico Precision@K por fold comparando os 5 métodos (para o post do dia 19)."""

import json
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

# carrega os 3 resultados
temas = json.load(open(ROOT / "data/resultados/backtest_temas.json", encoding="utf-8"))
tfidf = json.load(open(ROOT / "data/resultados/backtest_tfidf.json", encoding="utf-8"))

df_temas = pd.DataFrame(temas)
df_tfidf = pd.DataFrame(tfidf)

# merge por fold
merged = (
    df_tfidf[["fold", "precision@k", "k"]]
    .rename(columns={"precision@k": "TF-IDF"})
    .copy()
)
for bl in ("markov", "recência", "frequência", "recência_ponderada"):
    sub = df_temas[df_temas.baseline.eq(bl)].set_index("fold")["precision@k"].to_dict()
    merged[f"Baseline {bl[:10]}"] = merged.fold.map(sub)

# renomeia
cols = {
    "TF-IDF": "TF-IDF",
    "Baseline markov": "Markov",
    "Baseline recência": "Recência",
    "Baseline frequên": "Frequência",
    "Baseline recência_": "Rec. ponderada",
}
plot_df = merged.rename(columns=cols)

fig, axes = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [2, 1]})

# --- esquerda: Precision@K por fold ---
ax = axes[0]
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
plot_cols = [
    ("TF-IDF", "TF-IDF"),
    ("Baseline markov", "Markov"),
    ("Baseline recência", "Recência"),
    ("Baseline frequên", "Frequência"),
    ("Baseline recência_", "Rec. ponderada"),
]
for i, (col_key, col_label) in enumerate(plot_cols):
    if col_key in plot_df.columns:
        ax.plot(
            plot_df["fold"],
            plot_df[col_key],
            marker="o",
            label=col_label,
            color=colors[i],
            linewidth=2,
            markersize=6,
        )
ax.set_xlabel("Fold (ano de treino X)", fontsize=11)
ax.set_ylabel("Precision@K", fontsize=12)
ax.set_title("Precision@K por fold — 5 métodos", fontsize=13, fontweight="bold")
ax.legend(fontsize=9, loc="lower right")
ax.set_ylim(0.5, 1.05)
ax.axhline(y=0.82, color="gray", linestyle="--", alpha=0.3, label="_nolegend_")
ax.set_xticks(range(2017, 2026))
ax.set_xticklabels(range(2017, 2026), fontsize=9)
ax.tick_params(axis="y", labelsize=10)

# --- direita: médias ---
ax2 = axes[1]
med = (
    plot_df[[c for c in plot_df.columns if c != "fold"]]
    .mean()
    .sort_values(ascending=True)
)
bars = ax2.barh(med.index, med.values, color=colors[::-1], height=0.6)
ax2.set_xlabel("Precision@K (média dos folds)", fontsize=12)
ax2.set_xlim(0.5, 1.0)
for bar, val in zip(bars, med.values):
    ax2.text(
        bar.get_width() + 0.01,
        bar.get_y() + bar.get_height() / 2,
        f"{bar.get_width():.2f}",
        va="center",
        fontsize=11,
    )

fig.suptitle(
    "CACD Forecast AI — Backtesting Temporal (Precision@K por tema)\n",
    fontsize=13,
    fontweight="bold",
)
fig.tight_layout(pad=2.0)
out = ROOT / "docs/assets/precision_at_k.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"[ok] gráfico salvo: {out}")
