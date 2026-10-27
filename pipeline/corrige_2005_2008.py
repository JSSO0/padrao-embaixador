# -*- coding: utf-8 -*-
"""Correcoes da Fase D para 2005 (M1.7 + renumeracao) e 2008 (anulados).

2005 (verificado contra o PDF da prova):
  - remove q11-it5 e q16-it5 (fragmentos do inicio do Texto IV capturados
    como itens)
  - remove q17 (3 itens: discursiva da 2a etapa, "redija um texto")
  - remove q45, q48, q49 (discursivas: QUESTAO 45/49/50 - DISCURSIVA)
  - renumera a cauda deslocada: 39->40, 40->41, 41->42, 42->43, 46->47, 47->48
  - remove q43 (duplicata da prova 43)
  - zera answer das renumeradas (o gabarito sera re-aplicado)
  Pendencia: prova q46 (Haroldo de Campos, Poesia Concreta) nao foi
  transcrita — lacuna documentada (4 itens).

2008: q1.2, q45.2, q64.2 = ANULADOS oficiais (justificativa no PDF de
gabarito: "banca decide pela ANULAÇÃO do item") -> notes = "anulado".
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/processed/questions.parquet"

df = pd.read_parquet(PATH)
m05 = df.stage.eq("primeira_fase") & df.year.eq(2005)

# --- 1) remocoes verificadas ---------------------------------------------
rem = m05 & (
    (df.question_number.eq(11) & df.item_number.eq(5))
    | (df.question_number.eq(16) & df.item_number.eq(5))
    | (df.question_number.eq(17))
    | (df.question_number.eq(45))
    | (df.question_number.eq(48))
    | (df.question_number.eq(49))
    | (df.question_number.eq(43))
)
print(f"removendo de 2005: {int(rem.sum())} linhas")
print(df[rem].groupby("question_number").size().to_string())

# --- 2) renumeracao da cauda deslocada -----------------------------------
mapa = {39: 40, 40: 41, 41: 42, 42: 43, 46: 47, 47: 48}
ren = m05 & df.question_number.isin(list(mapa))
print(
    f"renumerando {int(ren.sum())} linhas: {sorted(df.loc[ren, 'question_number'].unique())}"
)
idx_ren = df.index[ren]
df.loc[idx_ren, "question_number"] = df.loc[idx_ren, "question_number"].map(mapa)
df.loc[idx_ren, "answer"] = None  # re-aplicar gabarito

# --- 3) 2008 anulados oficiais -------------------------------------------
m08 = df.stage.eq("primeira_fase") & df.year.eq(2008)
for qn in (1, 45, 64):
    sel = m08 & df.question_number.eq(qn) & df.item_number.eq(2) & df.answer.isna()
    for idx in df[sel].index:
        if pd.isna(df.at[idx, "notes"]) or not str(df.at[idx, "notes"]).strip():
            df.at[idx, "notes"] = "anulado"
            print(f"2008 q{qn} it2: marcado anulado (justificativa oficial)")

df = df[~rem].reset_index(drop=True)
df.to_parquet(PATH, index=False)
print(f"parquet: salvo ({len(df)} linhas)")
