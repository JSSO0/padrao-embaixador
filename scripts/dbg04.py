# -*- coding: utf-8 -*-
"""Debug 2004: blocos com coordenadas da pagina 2 (onde estao os itens 1-4)."""

import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, ".")
from parser.document_loader import load_pdf  # noqa: E402

pdf = Path("data/raw/CACD_2004/cursocacd/prova_objetiva_1__03e12b15.pdf")
doc = load_pdf(pdf, Path("."))
out = [f"paginas: {doc.n_pages}"]

# dump de blocos das paginas 2 e 3 (indices 1 e 2) com x0
import pymupdf as pm  # noqa: E402

pdf_doc = pm.open(pdf)
for pageno in (1, 2):
    page = pdf_doc[pageno]
    out.append(f"=== PAGINA {pageno + 1} (largura {page.rect.width:.0f}) ===")
    blocks = [b for b in page.get_text("blocks") if b[4].strip()]
    blocks.sort(key=lambda b: (round(b[1]), b[0]))
    for b in blocks[:40]:
        x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
        t = text.strip().replace("\n", " ⏎ ")[:90]
        out.append(f"  x0={x0:6.1f} x1={x1:6.1f} y0={y0:6.1f} | {t}")
pdf_doc.close()

Path("dbg04.txt").write_text("\n".join(out), encoding="utf-8")
print("ok")
