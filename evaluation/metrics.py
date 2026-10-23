"""Métricas de avaliação para o backtesting temporal do CACD.

Cada métrica opera sobre conjuntos de disciplinas: o conjunto previsto
(top-K temas sugeridos para X+1) e o conjunto real (as disciplinas que
de fato apareceram em X+1).
"""


def precision_at_k(predicted: set[str], actual: set[str], k: int) -> float:
    """Dos K temas previstos, quantos apareceram de fato."""
    top_k = set(list(predicted)[:k])
    if not top_k:
        return 0.0
    return len(top_k & actual) / len(top_k)


def recall_at_k(predicted: set[str], actual: set[str], k: int) -> float:
    """Dos temas que apareceram em X+1, quantos estavam nos K previstos."""
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
    """Normalized Discounted Cumulative Gain @ K (posicional)."""
    top_k = predicted[:k]
    dcg = sum(
        1.0 / __import__("math").log2(i + 2) for i, t in enumerate(top_k) if t in actual
    )
    ideal = min(len(actual), k)
    idcg = sum(1.0 / __import__("math").log2(i + 2) for i in range(ideal))
    return dcg / idcg if idcg > 0 else 0.0


def map_k(predicted: list[str], actual: set[str], k: int) -> float:
    """Mean Average Precision @ K (apenas 1 query por fold)."""
    hits = 0
    score = 0.0
    for i, t in enumerate(predicted[:k]):
        if t in actual:
            hits += 1
            score += hits / (i + 1)
    if not actual:
        return 0.0
    return score / min(len(actual), k)
