# -*- coding: utf-8 -*-
"""OCR posicional da tabela de gabarito 2006 (M1.6): letras por coluna."""

import io
import sys

import pymupdf
import pytesseract
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

doc = pymupdf.open("data/raw/CACD_2006/cursocacd/gabarito__e6a8a527.pdf")
page = doc[0]
clip = pymupdf.Rect(25, 310, 575, 405)
pix = page.get_pixmap(matrix=pymupdf.Matrix(4, 4), clip=clip)
img = Image.open(io.BytesIO(pix.tobytes("png")))
d = pytesseract.image_to_data(
    img, lang="eng", config="--psm 6", output_type=pytesseract.Output.DICT
)
out = []
for i in range(len(d["text"])):
    t = d["text"][i].strip()
    if t and d["conf"][i] > 30:
        x_pdf = 25 + d["left"][i] / 4.0
        y_pdf = 310 + d["top"][i] / 4.0
        print(f"y={y_pdf:6.1f} x={x_pdf:6.1f} conf={d['conf'][i]:3.0f} {t!r}")
