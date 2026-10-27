"""Baseline TF-IDF: similaridade de texto entre as provas do histórico e as
questões de X+1. Para cada fold X, fita o TF-IDF apenas com provas <= X.

Para cada tema (disciplina/topic) do histórico, calcula o centroid dos
vetores TF-IDF das suas questões. Para cada questão de X+1, encontra o
tema mais similar. O ranking de temas = a previsão.
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evaluation.metrics import precision_at_k, recall_at_k, f1_at_k, ndcg_at_k, map_k  # noqa: E402
from evaluation.baselines import BASELINES  # noqa: E402


def load_items(parquet: Path):
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
    ].copy()
    m["topic_key"] = m.discipline_canon + "/" + m.topic
    m["text"] = (m.question_text.fillna("") + " " + m.item_text.fillna("")).apply(
        lambda x: x[:2000]
    )
    return m


def tfidf_baseline(treino_items: pd.DataFrame, teste_items: pd.DataFrame) -> list[str]:
    """Fit TF-IDF no treino, calcula centroids por tema, classifica o teste."""
    from sklearn.feature_extraction.text import TfidfVectorizer

    treino_texts = (
        treino_items.question_text.fillna("") + " " + treino_items.item_text.fillna("")
    ).tolist()
    treino_topics = treino_items["topic_key"].tolist()
    teste_texts = (
        teste_items.question_text.fillna("") + " " + teste_items.item_text.fillna("")
    ).tolist()

    vectorizer = TfidfVectorizer(max_features=5000, stop_words=None)
    treino_vec = vectorizer.fit_transform(treino_texts)
    teste_vec = vectorizer.transform(teste_texts)

    # centroid por tema
    temas = sorted(set(treino_topics))
    centroids = {}
    for topic in temas:
        mask = [i for i, t in enumerate(treino_topics) if t == topic]
        if len(mask) > 0:
            centroids[topic] = np.asarray(treino_vec[mask].mean(axis=0)).flatten()

    # classifica cada questao de teste pelo tema mais próximo
    from sklearn.metrics.pairwise import cosine_similarity

    predictions = []
    for i in range(teste_vec.shape[0]):
        vec = teste_vec[i]
        best_topic, best_score = None, -1
        for topic, centroid in centroids.items():
            sim = cosine_similarity(vec, centroid.reshape(1, -1))[0][0]
            if sim > best_score:
                best_topic, best_score = topic, sim
        if best_topic:
            predictions.append(best_topic)
    return predictions


def main() -> None:
    parquet = ROOT / "data/processed/questions.parquet"
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
    ].copy()
    m["topic_key"] = m.discipline_canon + "/" + m.topic

    results = []
    for x in range(2017, 2026):
        treino = m[m.year.between(2006, x)]
        teste = m[m.year.eq(x + 1)]
        if teste.empty:
            continue

        actual = set(teste["topic_key"].unique())
        treino_items = treino

        # K = número de temas únicos que apareceram em X+1
        k = len(actual)

        # TF-IDF: prevê temas para X+1
        try:
            predicted_tfidf = tfidf_baseline(treino, teste)
        except Exception as e:
            print(f"  [!!] fold {x}: TF-IDF falhou: {e}")
            continue

        p = (
            precision_at_k(set(predicted_tfidf), actual, k)
            if (predicted_tfidf := predicted_tfidf)
            else 0.0
        )
        results.append(
            {
                "fold": x,
                "teste": x + 1,
                "k": k,
                "baseline": "tfidf",
                "precision@k": round(p, 4),
                "recall@k": round(recall_at_k(set(predicted_tfidf), actual, k), 4),
                "f1@k": round(f1_at_k(set(predicted_tfidf), actual, k), 4),
                "ndcg@k": round(ndcg_at_k(predicted_tfidf, actual, k), 4),
                "map@k": round(map_k(predicted_tfidf, actual, k), 4),
            }
        )
        print(f"  fold {x}: TF-IDF P@{k}={p:.2f}")

    out = ROOT / "data/resultados/backtest_tfidf.json"
    with out.open("w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)
    print(f"[ok] {out.name}: {len(results)} registros")


if __name__ == "__main__":
    main()
