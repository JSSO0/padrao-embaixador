# -*- coding: utf-8 -*-
"""Corrige as disciplinas de 2016 e 2019 conforme as secoes oficiais das
provas (M2.5 — erros de disciplina detectados na 2a validacao).

2016 (secoes oficiais da prova): q51-61 Historia Mundial; q62-73 Direito.
  O parquet tinha q56-59 Direito, q60-61 Direito e q65-73 Economia.
2019 (secoes oficiais IADES): q1-10 LP, q11-22 PI, q23-28 Geografia,
  q29-34 Direito/DIP, q35-43 LI, q44-54 HB, q55-65 HM, q66-73 Economia.
  O parquet marcava q29-34 como Geografia.
"""

import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/processed/questions.parquet"

CORRECOES = {
    "CACD_2016": {
        # qn: raw discipline (a canónica é derivada por canon_disc)
        **{qn: "História Mundial" for qn in range(56, 62)},
        **{qn: "Direito E Direito Internacional Público" for qn in range(62, 74)},
    },
    "CACD_2019": {
        **{qn: "Direito e Direito Internacional Público" for qn in range(29, 35)},
    },
}

df = pd.read_parquet(PATH)
m1 = df.stage.eq("primeira_fase")
total = 0
for contest, mapa in CORRECOES.items():
    for qn, nova in mapa.items():
        sel = m1 & df.contest_id.eq(contest) & df.question_number.eq(float(qn))
        antigo = df.loc[sel, "discipline"].iloc[0] if sel.any() else None
        if str(antigo) != nova:
            df.loc[sel, "discipline"] = nova
            df.loc[sel, "discipline_canon"] = None  # re-canonizar
            print(f"{contest} q{qn}: {antigo} -> {nova} ({int(sel.sum())} itens)")
            total += int(sel.sum())
df.to_parquet(PATH, index=False)
print(f"total: {total} itens corrigidos")
