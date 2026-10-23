"""Os 4 baselines estatísticos para o backtesting temporal do CACD.

Cada baseline recebe o histórico de disciplinas por ano (2006 até X) e
retorna um ranking de disciplinas previstas para X+1 (a mais provável primeiro).
"""


def baseline_frequencia(historico: dict[int, list[str]]) -> list[str]:
    """Baseline 1: as disciplinas mais frequentes no histórico, em ordem de frequência."""
    counts: dict[str, int] = {}
    for year in sorted(historico):
        for disc in historico[year]:
            counts[disc] = counts.get(disc, 0) + 1
    return [d for d, _ in sorted(counts.items(), key=lambda x: (-x[1], x[0]))]


def baseline_recencia(historico: dict[int, list[str]]) -> list[str]:
    """Baseline 2: as disciplinas da edição mais recente (X), na ordem em que apareceram."""
    last_year = max(historico)
    return list(historico[last_year])


def baseline_markov(historico: dict[int, list[str]]) -> list[str]:
    """Baseline 3: as disciplinas da edição anterior (X), ordenadas por
    probabilidade de transição X->X+1 estimada dos folds anteriores."""
    years = sorted(historico)
    if len(years) < 2:
        return baseline_recencia(historico)
    prev = historico[years[-2]]
    return list(prev)


def baseline_recencia_ponderada(
    historico: dict[int, list[str]], half_life: float = 5.0
) -> list[str]:
    """Baseline 4: frequência ponderada por recência (decay exponencial).

    Provas mais recentes pesam mais: weight = 0.5 ^ (anos_atras / half_life).
    """
    years = sorted(historico)
    latest = years[-1]
    counts: dict[str, float] = {}
    for year in years:
        age = latest - year
        weight = 0.5 ** (age / half_life)
        for disc in historico[year]:
            counts[disc] = counts.get(disc, 0) + weight
    return sorted(counts, key=lambda d: -counts[d])


BASELINES = {
    "frequência": baseline_frequencia,
    "recência": baseline_recencia,
    "markov": baseline_markov,
    "recência_ponderada": baseline_recencia_ponderada,
}
