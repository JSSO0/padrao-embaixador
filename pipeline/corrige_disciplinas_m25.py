# -*- coding: utf-8 -*-
"""Corrige as disciplinas por questao conforme as secoes oficiais das provas
(mapa CAPS/uppercase dos PDFs — M2.5, 3a rodada)."""

import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/processed/questions.parquet"

# raw labels (canon e derivado por canon_disc)
CORRECOES = {
    "CACD_2015": {
        26: "Política Internacional",
        66: "Direito E Direito Internacional Público",
        67: "Direito E Direito Internacional Público",
    },
    "CACD_2016": {
        12: "Língua Portuguesa",
        13: "Língua Portuguesa",
        14: "Língua Portuguesa",
        68: "Economia",
        69: "Economia",
        70: "Economia",
        71: "Economia",
        72: "Economia",
        73: "Economia",
    },
    "CACD_2017": {
        8: "Língua Portuguesa",
        9: "Língua Portuguesa",
        10: "Língua Portuguesa",
        21: "Política Internacional",
        22: "Política Internacional",
        27: "Geografia",
        28: "Geografia",
        54: "História do Brasil",
    },
    "CACD_2018": {28: "Geografia", 53: "História do Brasil", 54: "História do Brasil"},
    "CACD_2024": {
        9: "Língua Portuguesa",
        10: "Língua Portuguesa",
        20: "Política Internacional",
        47: "História do Brasil",
        48: "História do Brasil",
        49: "História do Brasil",
        58: "História Mundial",
    },
}

df = pd.read_parquet(PATH)
m1 = df.stage.eq("primeira_fase")
total = 0
for contest, mapa in CORRECOES.items():
    for qn, nova in mapa.items():
        sel = m1 & df.contest_id.eq(contest) & df.question_number.eq(float(qn))
        if not sel.any():
            continue
        antigo = df.loc[sel, "discipline"].iloc[0]
        df.loc[sel, "discipline"] = nova
        df.loc[sel, "discipline_canon"] = None
        print(f"{contest} q{qn}: {antigo} -> {nova} ({int(sel.sum())} itens)")
        total += int(sel.sum())
df.to_parquet(PATH, index=False)
print(f"total: {total} itens corrigidos")
