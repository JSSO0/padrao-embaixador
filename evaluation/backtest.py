"""Backtesting temporal do CACD: janela expansiva, 9 folds (X = 2017 a 2025).

Para cada fold X:
  - Treino: todas as provas de 2006 a X (o histórico de disciplinas por ano)
  - Teste: as disciplinas que de fato apareceram em X+1
  - Baselines: cada baseline prevê o ranking de disciplinas para X+1
  - Métricas: Precision@K, Recall@K, F1@K, NDCG@K, MAP@K

O K é calibrado ao nº médio de disciplinas que apareceram por edição no
treino (a media das fases 2006-X).
"""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evaluation.metrics import precision_at_k, recall_at_k, f1_at_k, ndcg_at_k, map_k  # noqa: E402
from evaluation.baselines import BASELINES  # noqa: E402


def load_disciplines(parquet: Path) -> dict[int, list[str]]:
    """{ano: [disciplinas canonizadas únicas, ordenadas alfabeticamente]}"""
    df = pd.read_parquet(parquet)
    m = df[
        df.stage.eq("primeira_fase")
        & df.discipline_canon.notna()
        & df.discipline_canon.astype(str).str.strip().ne("")
        & df.discipline_canon.str.match(r"^[A-ZÀ-Ú]", na=False)
    ]
    by_year = (
        m.groupby("year")["discipline_canon"].apply(lambda x: sorted(set(x))).to_dict()
    )
    return by_year


def run_backtest(parquet: Path, output_dir: Path) -> list[dict]:
    """Executa os 9 folds e retorna os resultados por fold × baseline."""
    historico_full = load_disciplines(parquet) if False else load_disciplines(parquet)
    results = []
    for x in range(2017, 2026):
        treino = {y: d for y, d in historico_full.items() if 2006 <= y <= x}
        actual = set(historico_full.get(x + 1, []))
        if not actual:
            print(f"    [!!] X+1 = {x + 1}: sem dados de teste")
            continue
        # K = nº médio de disciplinas por edição no treino
        k = round(sum(len(d) for d in treino.values()) / len(treino)) if treino else 8
        for bl_name, bl_fn in __import__(
            "evaluation.baselines", fromlist=["BASELINES"]
        ).BASELINES.items():
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
                    "previsto": predicted[:k],
                    "real": sorted(actual),
                }
            )
            print(
                f"  fold {x}: {bl_name:22} P@{k}={p:.2f} R@{k}={r:.2f} F1={f1:.2f} NDCG={nd:.2f} MAP={mk:.2f}"
            )
    return results


def precision_at_k(predicted: set[str], actual: set[str], k: int) -> float:
    top_k = set(list(predicted)[:k])
    if not top_k:
        return 0.0
    return len(top_k & actual) / len(top_k)


def recall_at_k(predicted: set[str], actual: set[str], k: int) -> float:
    top_k = set(list(predicted)[:k])
    if not actual:
        return 0.0
    return len(top_k & actual) / len(actual)


def f1_at_k(predicted: set[str], actual: set[str], k: int) -> float:
    p = precision_at_k(predicted, actual, k)
    r = recall_at_k(predicted, actual, k)
    if p + r == 0:
        return 0.0
    return 2 * p * r / (p + r)


def ndcg_at_k(predicted: list[str], actual: set[str], k: int) -> float:
    import math

    top_k = predicted[:k]
    dcg = sum(
        1.0 / __import__("math").log2(i + 2) for i, t in enumerate(top_k) if t in actual
    )
    ideal = min(len(actual), k)
    idcg = sum(1.0 / __import__("math").log2(i + 2) for i in range(ideal))
    return dcg / idcg if idcg > 0 else 0.0


def map_k(predicted: list[str], actual: set[str], k: int) -> float:
    import math

    hits = 0
    score = 0.0
    for i, t in enumerate(predicted[:k]):
        if t in actual:
            hits += 1
            score += hits / (i + 1)
    return score / min(len(actual), k) if actual else 0.0


if __name__ == "__main__":
    from evaluation.metrics import (
        precision_at_k as pk,
        recall_at_k as rk,
        f1_at_k as fk,
        ndcg_at_k as nk,
        map_k as mk,
    )

    parquet = ROOT / "data/processed/questions.parquet"
    hist = load_disciplines(parquet)
    print("histórico por ano:", {y: len(d) for y, d in sorted(hist.items())})
    results = run_backtest(parquet, ROOT / "evaluation")
    out = ROOT / "data/processed/backtest_results.json"
    import json

    out.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[ok] {out}")
