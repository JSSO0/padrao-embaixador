# -*- coding: utf-8 -*-
"""OCR celula a celula da coluna q4 do gabarito 2006 (M1.6)."""

import io
import sys

import pymupdf
import pytesseract
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

doc = pymupdf.open("data/raw/CACD_2006/cursocacd/gabarito__e6a8a527.pdf")
page = doc[0]
# coluna q4: x ~80-95 (header em 87.0); linhas: item1 y~336, item2 ~355,
# '+' ~362, item3 ~373, item4 ~391
bands = [
    ("item 1", 330, 346),
    ("item 2", 352, 361),
    ("+     ", 360, 370),
    ("item 3", 370, 382),
    ("item 4", 386, 400),
]
for nome, y0, y1 in bands:
    clip = pymupdf.Rect(76, y0, 100, y1)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(8, 8), clip=clip)
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
    txt = pytesseract.image_to_string(
        img, lang="eng", config="--psm 10 -c tessedit_char_whitelist=+XABCDE"
    ).strip()
    print(f"{nome}: {txt!r}")
