"""Dump integral: acha marcadores via finditer (tolerante) e mostra o bloco cru."""

import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
RE_MARK = re.compile(r"QUEST.{0,3}O\s*(\d{1,3})", re.I)

CASES = [
    ("data/raw/CACD_2003/archive/Primeira_Fase_Objetiva .pdf", 11, 15),
    ("data/raw/CACD_2005/archive/CESPE-2005-IRBR-Diplomata.pdf", 9, 12),
]
for rel, q_from, q_to in CASES:
    p = ROOT / rel
    with pymupdf.open(p) as doc:
        full = "".join(pg.get_text("text") for pg in doc)
    marks = sorted((m.start(), int(m.group(1))) for m in RE_MARK.finditer(full))
    starts = [s for s, n in marks if n == q_from]
    print("=" * 30, f"{rel.split('/')[-1]}: QUESTAO {q_from} -> {q_to}")
    if not starts:
        print(
            "  marcador",
            q_from,
            "NAO encontrado; presentes:",
            sorted({n for _, n in marks}),
        )
        continue
    ends = [s for s, n in marks if s > starts[0] and n == q_to]
    if not ends:
        print("  fim", q_to, "NAO encontrado; usando 1200 chars")
        ends = [starts[0] + 1200]
    print(full[starts[0] : ends[0]])
    print()
