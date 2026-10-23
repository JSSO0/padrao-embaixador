"""Backtesting temático: Precision@K por TOPIC (não por disciplina).

Agora o 'tema' é a combinacao disciplina+topic (ex: 'HB/era_vargas',
'PI/ONU_multilateral'). O K é o nº médio de temas por edição.

Reutiliza a infraestrutura do backtest.py (janela expansiva, 9 folds).
"""

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evaluation.metrics import precision_at_k, recall_at_k, f1_at_k, ndcg_at_k, map_k  # noqa: E402
from evaluation.baselines import BASELINES  # noqa: E402


def load_topics(parquet: Path) -> dict[int, list[str]]:
    """{ano: [temas únicos = disciplina/topic, ordenados]}"""
    df = pd.read_parquet(parquet)
    m = df[
        df.stage.eq("primeira_fase")
        & df.discipline_canon.notna()
        & df.topic.notna()
        & df.topic.ne("geral")
        & df.discipline_canon.isin(
            [
                "Língua Portuguesa",
                "Política Internacional",
                "História Mundial",
                "Língua Inglesa",
                "História do Brasil",
                "Economia",
                "Geografia",
                "Direito",
            ]
        )
    ]
    m = m.copy()
    m["topic_key"] = m.discipline_canon + "/" + m.topic
    by_year = m.groupby("year")["topic_key"].apply(lambda x: sorted(set(x))).to_dict()
    return by_year


def run_theme_backtest(parquet: Path) -> list[dict]:
    historico = load_topics(parquet)
    results = []
    for x in range(2017, 2026):
        treino = {y: d for y, d in historico.items() if 2006 <= y <= x}
        actual = set(historico.get(x + 1, []))
        if not actual:
            continue
        k = round(sum(len(d) for d in treino.values()) / len(treino))
        for bl_name, bl_fn in BASELINES.items():
            predicted = bl_fn(treino)
            p = precision_at_k(set(predicted), actual, k)
            r = recall_at_k(set(predicted), actual, k)
            f1 = f1_at_k(set(predicted), actual, k)
            nd = ndcg_at_k(predicted, actual, k)
            mk = map_k(predicted, actual, k)
            results.append(
                {
                    "fold": x,
                    "teste": x + 1,
                    "k": k,
                    "baseline": bl_name,
                    "precision@k": round(p, 4),
                    "recall@k": round(r, 4),
                    "f1@k": round(f1, 4),
                    "ndcg@k": round(nd, 4),
                    "map@k": round(mk, 4),
                    "n_temas_reais": len(actual),
                    "n_temas_previstos": len(predicted),
                }
            )
    return results


def summary(results: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(results)
    med = df.groupby("baseline")[
        ["precision@k", "recall@k", "f1@k", "ndcg@k", "map@k"]
    ].mean()
    return med


if __name__ == "__main__":
    print("=" * 60)
    print("BACKTESTING TEMÁTICO — Precision@K por tema (disciplina/topic)")
    print("=" * 60)
    parquet = ROOT / "data/processed/questions.parquet"
    historico = load_topics(parquet)
    print("temas por ano:", {y: len(t) for y, t in sorted(historico.items())})
    print()
    results = run_theme_backtest(parquet)
    print()
    med = summary(results)
    print("== Médias por baseline (temas) ==")
    print(med.to_string(float_format=lambda v: f"{v:.2f}"))
    print()

    df = pd.DataFrame(results)
    piv = df.pivot_table(index="fold", columns="baseline", values="precision@k")
    print("== Precision@K por fold × baseline (temas) ==")
    print(piv.to_string(float_format=lambda v: f"{v:.2f}"))

    print("\n== Insights ==")
    best = med["precision@k"].idxmax()
    print(
        f"  Melhor baseline: {best} (Precision@K = {med.loc[best, 'precision@k']:.2f})"
    )
    print(
        f"  Nº médio de temas por edição: {df.groupby('fold')['k'].first().mean():.0f}"
    )
    print(f"  O que isso NÃO prova: que temas específicos dentro de um tema")
    print(f"  (ex: 'Guerra do Paraguai' dentro de 'Império') seguem o mesmo padrão.")
    print(f"  Também não prova que a questão literal pode ser prevista.")

    out = ROOT / "data/processed/backtest_temas.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n[ok] {out}")
