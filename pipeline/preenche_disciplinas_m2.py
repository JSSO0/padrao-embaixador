# -*- coding: utf-8 -*-
"""Preenche a disciplina das 72 linhas da 1a fase sem discipline (M2.2/B1).

Verificado por estrutura da prova e conteudo:
  - CACD_2003 q11-14 (20 linhas): bloco entre Inglês (q10) e História (q15),
    conteudo de economia internacional (leste asiatico, OMC, Estado
    desenvolvimentista) -> "Economia"
  - CACD_2005 q9-11 e q15-16 (20 linhas): entre questoes de Historia Mundial
    (q8, q14); conteudo de imperialismo, entreguerras e Segunda Guerra
    -> "História" (rotulo usado pela edicao; canônico = História Mundial)
  - CACD_2007 q31-38 (32 linhas): 2a etapa, Historia do Brasil (coronelismo,
    Vargas, regime militar, Plano Cruzado, MERCOSUL) -> "História do Brasil"
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/processed/questions.parquet"

MAPA = {
    "CACD_2003": {"qns": [11, 12, 13, 14], "discipline": "Economia"},
    "CACD_2005": {"qns": [9, 10, 11, 15, 16], "discipline": "História"},
    "CACD_2007": {
        "qns": [31, 32, 33, 34, 35, 36, 37, 38],
        "discipline": "História do Brasil",
    },
}

df = pd.read_parquet(PATH)
total = 0
for contest, info in MAPA.items():
    sel = (
        df.stage.eq("primeira_fase")
        & df.contest_id.eq(contest)
        & df.discipline.isna()
        & df.question_number.isin(info["qns"])
    )
    n = int(sel.sum())
    df.loc[sel, "discipline"] = info["discipline"]
    print(f"{contest}: {n} linhas -> {info['discipline']}")
    total += n
df.to_parquet(PATH, index=False)
print(f"ok: {total} disciplinas preenchidas")
