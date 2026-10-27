# -*- coding: utf-8 -*-
"""Forense das tabelas de gabarito TPS: dump de celulas (y, x, texto) para
reconstruir colunas que o parser perdeu (M1.6)."""

import sys
from pathlib import Path

import pymupdf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[2]
YEARS = {
    "2005": "cursocacd/gabarito__4031719e.pdf",
    "2006": "cursocacd/gabarito__e6a8a527.pdf",
    "2010": "cursocacd/gabarito__81a90c50.pdf",
    "2011": "archive/Gabarito.pdf",
}
year = sys.argv[1]
path = ROOT / "data" / "raw" / f"CACD_{year}" / YEARS[year]
doc = pymupdf.open(path)
for pno, page in enumerate(doc):
    spans = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip()
                if t:
                    spans.append((s["bbox"][1], s["bbox"][0], s["bbox"][2], t))
    spans.sort()
    rows = []
    for y0, x0, x1, t in spans:
        if rows and abs(rows[-1][0][0] - y0) <= 3.0:
            rows[-1].append((x0, x1, t))
        else:
            rows.append([(x0, x1, t)])
    # primeira linha = y0
    print(f"\n=== {year} pagina {pno}: {len(rows)} linhas ===")
    for r in rows:
        cells = " | ".join(f"{x0:.0f}:{t}" for x0, _, t in r)
        print(cells[:200])
