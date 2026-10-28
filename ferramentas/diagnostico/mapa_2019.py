# -*- coding: utf-8 -*-
"""Mapa de secoes 2019 (prova 2): questao -> ultima secao anterior."""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = Path(
    "data/processed/text/CACD_2019/cursocacd/prova_objetiva_2__bf883c10.txt"
).read_text(encoding="utf-8", errors="replace")
t2 = re.sub(r"\s+", " ", t)
SEC = r"(L[íi]ngua Inglesa|Hist[óo]ria do Brasil|Hist[óo]ria Mundial|Economia|Direito)"
events = []
for m in re.finditer(SEC + r"|QUEST.{0,4}O\s+(\d{1,3})\b", t2):
    if m.group(1):
        events.append((m.start(), "SEC", m.group(1)))
    else:
        events.append((m.start(), "Q", int(m.group(2))))
atual = None
mapa = {}
for pos, tipo, val in events:
    if tipo == "SEC":
        atual = val
    elif isinstance(val, int) and 30 <= val <= 73:
        mapa.setdefault(val, atual)
for qn in sorted(mapa):
    print(f"q{qn}: {mapa[qn]}")
