# -*- coding: utf-8 -*-
"""Extrai os itens 'Tema errado' da 2a validacao M2.5 com origem e texto."""

import re
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
md = (ROOT / "data/processed/qa_sample/validacao_temas_m2.md").read_text(
    encoding="utf-8"
)
df = pd.read_parquet(ROOT / "data/processed/questions.parquet")

blocos = md.split("## ")[1:]
for b in blocos:
    if "[x] Tema errado" not in b:
        continue
    cab = b.splitlines()[0].strip()
    m = re.match(r"(CACD_\d+) · Q(\d+)", cab)
    contest, qn = m.group(1), int(m.group(2))
    itn = re.search(r"· item (\d+)", cab)
    tema = re.search(r"Tema atribuído:\*\* `([^`]+)` \(([^)]+)\)", b)
    correto = re.search(r"correto:\s*(.+)", b)
    texto = re.search(r"\*\*Texto do item:\*\* (.+)", b)
    sel = df[
        (df.stage == "primeira_fase")
        & (df.contest_id.eq(contest))
        & (df.question_number.eq(int(qn)))
    ]
    if itn:
        sel = sel[sel.item_number.eq(float(itn.group(1)))]
    r = sel.iloc[0] if len(sel) else None
    print(f"{cab} | atribuido: {tema.group(1)} ({tema.group(2)})")
    print(f"   correto: {correto.group(1).strip()}")
    if r is not None:
        print(f"   texto: {re.sub(chr(10), ' ', str(r['question_text']))[:120]}")
    print()
