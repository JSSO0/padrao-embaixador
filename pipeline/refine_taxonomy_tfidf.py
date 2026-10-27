"""Refina a taxonomia usando TF-IDF: cada item 'geral' é re-classificado
pelo tema cujo centroide semântico é mais próximo.

Também divide os temas existentes em sub-temas mais específicos usando
a similaridade de texto dentro de cada tema.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/processed/questions.parquet"
df = pd.read_parquet(PATH)
m = (
    df.stage.eq("primeira_fase")
    & df.discipline_canon.notna()
    & df.topic.notna()
    & df.topic.ne("geral")
)

# 1) Identifica os itens "geral" que têm texto suficiente
g_geral = df[
    df.stage.eq("primeira_fase") & df.topic.eq("geral") & df.discipline_canon.notna()
].copy()
print(f"itens 'geral' para re-classificar: {len(g_geral)}")

# 2) Para cada disciplina, re-classifica os itens "geral" pelo texto
for disc in sorted(g_geral.discipline_canon.unique()):
    sub_geral = g_geral[g_geral.discipline_canon.eq(disc)]
    # pega os temas existentes para essa disciplina
    temas_existentes = sorted(
        df[
            df.stage.eq("primeira_fase")
            & df.discipline_canon.eq(disc)
            & df.topic.notna()
            & df.topic.ne("geral")
        ]["topic"].unique()
    )
    if not temas_existentes:
        continue

    # textos de treino (itens com tema específico) e de teste (itens "geral")
    treino = df[
        df.stage.eq("primeira_fase")
        & df.discipline_canon.eq(disc)
        & df.topic.ne("geral")
        & df.topic.notna()
    ]
    treino_texts = (
        treino.question_text.fillna("") + " " + treino.item_text.fillna("")
    ).tolist()
    treino_topics = treino["topic"].tolist()
    geral_texts = (
        g_geral[g_geral.discipline_canon.eq(disc)].question_text.fillna("")
        + " "
        + g_geral[g_geral.discipline_canon.eq(disc)].item_text.fillna("")
    ).tolist()

    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorizer = TfidfVectorizer(max_features=3000)
    treino_vec = vectorizer.fit_transform(treino_texts)
    geral_vec = vectorizer.transform(geral_texts)

    # centroid por tema
    temas = sorted(set(treino_topics))
    centroids = {}
    for topic in temas:
        mask = [i for i, t in enumerate(treino_topics) if t == topic]
        if mask:
            centroids[topic] = np.asarray(treino_vec[mask].mean(axis=0)).flatten()

    from sklearn.metrics.pairwise import cosine_similarity

    # re-classifica cada item "geral"
    for j, (i_global, row) in enumerate(
        g_geral[g_geral.discipline_canon.eq(disc)].iterrows()
    ):
        vec = geral_vec[j]
        best_topic, best_sim = None, -1
        for topic, centroid in centroids.items():
            sim = cosine_similarity(vec, centroid.reshape(1, -1))[0][0]
            if sim > best_sim:
                best_topic, best_sim = topic, sim
        if best_topic and best_sim > 0.05:
            df.at[i_global, "topic"] = best_topic

df.to_parquet(PATH, index=False)

# relatório
print("\n=== Taxonomia pós-refinamento TF-IDF ===")
geral_total = 0
for disc in sorted(
    df[df.stage.eq("primeira_fase") & df.discipline_canon.notna()][
        "discipline_canon"
    ].unique()
):
    sub = df[df.stage.eq("primeira_fase") & df.discipline_canon.eq(disc)]
    c = sub["topic"].value_counts().to_dict()
    g = c.pop("geral", 0)
    geral_total += g
    print(f"  {disc}: {c} | geral: {g}")
print(f"  TOTAL geral: {geral_total}")
