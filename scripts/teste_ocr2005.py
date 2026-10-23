"""Teste de OCR: grid do gabarito 2005 (a primeira pagina) vs extracao nativa."""

import io
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pytesseract
from PIL import Image

pdf = ROOT / "data/raw/CACD_2005/cursocacd/gabarito__4031719e.pdf"
with pymupdf.open(pdf) as doc:
    pg = doc[0]
    pix = pg.get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    txt = pytesseract.image_to_string(img, lang="eng", config="--psm 6")
    nat = pg.get_text("text")

print("=== OCR (primeiras 30 linhas nao vazias) ===")
n = 0
for ln in txt.split("\n"):
    if ln.strip():
        print("   ", ln.strip()[:110])
        n += 1
        if n >= 25:
            break
print()
print("=== NATIVO (primeiras 25 linhas nao vazias) ===")
n = 0
for ln in nat.split("\n"):
    if ln.strip():
        print("   ", ln.strip()[:110])
        n += 1
        if n >= 25:
            break
