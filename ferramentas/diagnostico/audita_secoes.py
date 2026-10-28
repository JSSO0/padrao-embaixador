# -*- coding: utf-8 -*-
"""Audita secoes de disciplina nas provas (M2): mapeia qn -> secao a partir
dos cabecalhos de secao dos textos extraidos."""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]

SEC = r"(LÍNGUA INGLESA|LÍNGUA PORTUGUESA|HISTÓRIA DO BRASIL|HISTÓRIA MUNDIAL|POLÍTICA INTERNACIONAL|GEOGRAFIA|NOÇÕES DE DIREITO E DIREITO INTERNACIONAL PÚBLICO|NOÇÕES DE ECONOMIA E DE ECONOMIA INTERNACIONAL|CULTURA GERAL)"

for contest, files in {
    "CACD_2016": ["cursocacd/prova_objetiva_2__d6d5c0ec.txt"],
    "CACD_2019": ["cursocacd/prova_objetiva_2__bf883c10.txt"],
}.items():
    print(f"=== {contest}")
    for rel in files:
        t = (ROOT / "data/processed/text" / contest / rel).read_text(
            encoding="utf-8", errors="replace"
        )
        t2 = re.sub(r"\s+", " ", t)
        events = []
        for m in re.finditer(SEC + r"|QUEST.{0,4}O\s+(\d{1,3})\b", t2):
            if m.group(1):
                events.append((m.start(), "SEC", m.group(1)[:40]))
            else:
                events.append((m.start(), "Q", m.group(2)))
        # para cada questao, qual a ultima secao antes dela
        atual = None
        mapa = {}
        for pos, tipo, val in events:
            if tipo == "SEC":
                atual = val
            else:
                qn = int(val)
                mapa.setdefault(qn, atual)
        for qn in sorted(mapa):
            print(f"  q{qn}: {mapa[qn]}")
