# -*- coding: utf-8 -*-
"""Extrai os itens marcados 'Tema errado' da validacao M2.5."""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
md = (
    Path(__file__).resolve().parents[2]
    / "data/processed/qa_sample/validacao_temas_m2.md"
).read_text(encoding="utf-8")
blocos = md.split("## ")[1:]
for b in blocos:
    if "[x] Tema errado" in b:
        cab = b.splitlines()[0].strip()
        tema = re.search(r"Tema atribuído:\*\* `([^`]+)`", b)
        correto = re.search(r"correto:\s*(.+)", b)
        disc = re.search(r"\*\*Disciplina:\*\* ([^\n]+)", b)
        print(
            f"{cab} | atribuido: {tema.group(1) if tema else '?'} | correto: {correto.group(1).strip() if correto else '?'} | {disc.group(1) if disc else ''}"
        )
