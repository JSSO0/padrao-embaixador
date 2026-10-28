# -*- coding: utf-8 -*-
"""Dump dos cabecalhos CAPS + questoes (para mapear secoes de uma edicao)."""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
f = (
    Path(__file__).resolve().parents[2]
    / "data/processed/text/CACD_2015/cursocacd/prova_objetiva_2__8f71eac6.txt"
)
t = f.read_text(encoding="utf-8", errors="replace")
for i, l in enumerate(t.splitlines(), 1):
    s = l.strip()
    letras = [c for c in s if c.isalpha()]
    if letras and all(c.isupper() for c in letras) and 4 < len(s) < 60:
        print(f"{i}: {s}")
    if "QUESTÃO 6" in s.upper() or "QUESTÃO 7" in s.upper():
        print(f"{i}: {s[:45]}")
