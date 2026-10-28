# -*- coding: utf-8 -*-
"""Mapa de secoes da prova 2017 (prova 1 e 2)."""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
for rel in ("prova_objetiva_1__f9bedc4f.txt", "prova_objetiva_2__b083db41.txt"):
    t = (ROOT / "data/processed/text/CACD_2017/cursocacd" / rel).read_text(
        encoding="utf-8", errors="replace"
    )
    t2 = re.sub(r"\s+", " ", t)
    print(f"=== {rel} (len {len(t2)})")
    SEC = r"(L[íi]ngua Portuguesa|L[íi]ngua Inglesa|Hist[óo]ria do Brasil|Hist[óo]ria Mundial|Pol[íi]tica Internacional|Geografia|No[çc][õo]es de Direito[^A-Z]*|No[çc][õo]es de Economia[^A-Z]*|Economia)"
    events = []
    for m in re.finditer(SEC + r"|QUEST.{0,4}O\s+(\d{1,3})\b", t2, re.I):
        if m.group(1):
            events.append(("SEC", m.group(1)))
        else:
            events.append(("Q", int(m.group(2))))
    atual = None
    for tipo, val in events:
        if tipo == "SEC":
            atual = val
            print(f"  SECÇÃO: {val}")
        elif 1 <= val <= 73:
            pass
    # imprime mapping final
    mapa = {}
    for tipo, val in events:
        if tipo == "SEC":
            atual = val
        else:
            mapa.setdefault(val, atual)
    print("  ", {q: (mapa[q] or "?")[:18] for q in sorted(mapa)})
