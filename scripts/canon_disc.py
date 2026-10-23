"""Normaliza as disciplinas dos 5.038 itens da 1a fase para o conjunto canonico
e gera o parquet atualizado. Necessario antes do backtesting (Precision@K)."""

import re
from pathlib import Path

import pandas as pd

PATH = "data/processed/questions.parquet"
df = pd.read_parquet(PATH)
m = df.stage.eq("primeira_fase")


def canon(d: str | None) -> str | None:
    if pd.isna(d) or not str(d).strip():
        return None
    u = re.sub(r"\s+", " ", str(d).strip().upper())
    m = [
        (r"PORTUGU.*|L.*NGUA PORTUGUESA|L.*NEA PORTUGUESA", "Língua Portuguesa"),
        (r"INGL.*", "Língua Inglesa"),
        (r"HIST.*BRASIL", "História do Brasil"),
        (r"HIST.*MUNDIAL|HIST.*GERAL|^HIST[^O]", "História Mundial"),
        (r"GEOGRAF", "Geografia"),
        (r"POL.*TICA INTERNACIONAL", "Política Internacional"),
        (r"POLITICA|^POL\b", "Política Internacional"),
        (r"ECONOM", "Economia"),
        (r"DIREITO", "Direito"),
        (r"ESPANHOL|FRANC", "Espanhol e Francês"),
        (r"ALEM", "Alemão"),
    ]
    for pat, val in m:
        if re.search(pat, u):
            return val
    return str(d).strip()


df.loc[m, "discipline_canon"] = df.loc[m, "discipline"].apply(canon)
df.to_parquet(PATH, index=False)
print("disciplinas canonizadas:")
print(df[df.stage.eq("primeira_fase")].discipline_canon.value_counts().to_string())
