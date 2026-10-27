# -*- coding: utf-8 -*-
"""Registra a anulacao da questao 4 (MC) do TPS 2006 (M1.7/M1.6).

Evidencia: no gabarito oficial definitivo (caderno Alfa, data 11/2/2006), a
linha de multipla escolha ("+") tem a celula da questao 4 preenchida com "+",
o mesmo marcador de anulacao do gabarito 2008 (onde as justificativas oficiais
confirmam: celula "+" = item anulado). As 28 demais celulas da linha tem letras
validas (D/C/A/E/B) e estao no cache; a q4 nao tem letra — foi anulada.
"""

from pathlib import Path

import pandas as pd

PATH = Path(__file__).resolve().parents[1] / "data/processed/questions.parquet"

df = pd.read_parquet(PATH)
m = (
    df.stage.eq("primeira_fase")
    & df.year.eq(2006)
    & df.question_number.eq(4)
    & df.answer.isna()
)
for idx in df[m].index:
    df.at[idx, "notes"] = "anulado"
    print(
        f"2006 q4 it{df.at[idx, 'item_number']}: marcado anulado ('+' na linha MC do gabarito oficial)"
    )
df.to_parquet(PATH, index=False)
print("ok")
