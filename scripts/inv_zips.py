"""Inventario de qualidade de texto: todos os PDFs de prova escrita 2003-2012."""

import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
CIPHER_HINT = "HBLOISHMCTUI"

for y in range(2003, 2013):
    folder = ROOT / "data/raw" / f"CACD_{y}" / "archive"
    if not folder.exists():
        continue
    print("=" * 15, y)
    for p in sorted(folder.glob("*.pdf")):
        if re.search(r"Gab|gabarito|GAB", p.stem):
            continue
        with pymupdf.open(p) as doc:
            t = "".join(pg.get_text("text") for pg in doc)
            npages = len(doc)
        qs = len(re.findall(r"QUEST[ÃA]O\s*\d+|Quest[ãa]o\s+\d+", t))
        cipher = CIPHER_HINT in t or "HBLOISH" in t
        tag = "CIPHER" if cipher else ("ok" if len(t) > 8000 else "POUCO TEXTO")
        print(f"   {npages:3}p {len(t):6}c {tag:12} q={qs:2} | {p.stem[:46]}")
