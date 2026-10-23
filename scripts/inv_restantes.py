"""Inventario final: o que falta por ano em TODAS as fases."""

import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]

for y in range(2003, 2013):
    folder = ROOT / "data/raw" / f"CACD_{y}" / "archive"
    if not folder.exists():
        continue
    print("=" * 12, y)
    for p in sorted(folder.glob("*.pdf")):
        if re.search(r"Gab|gabarito|GAB|TPS.*Gab", p.stem, re.I):
            continue
        with pymupdf.open(p) as doc:
            t = "".join(pg.get_text("text") for pg in doc)
            npages = len(doc)
        qs = len(re.findall(r"QUEST[ÃA]O\s*\d+|Quest[ãa]o\s+\d+", t))
        tag = "CIPHER" if "HBLOISH" in t else ("ok" if len(t) > 8000 else "POUCO")
        print(f"   {npages:2}p {len(t):6}c {tag:8} q={qs:2} | {p.stem[:52]}")
