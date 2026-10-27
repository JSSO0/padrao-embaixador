"""Debug do OCR 2009 HB: por pagina, native len, RASCUNHO, QUESTAO, OCR rodado."""

import io
import os
import sys
from pathlib import Path

import pymupdf

os.environ["TESSDATA_PREFIX"] = str(Path(os.environ["LOCALAPPDATA"]) / "tessdata")
os.environ["PATH"] += r";C:\Program Files\Tesseract-OCR"
import pytesseract  # noqa: E402
from PIL import Image  # noqa: E402

pdf = Path(__file__).resolve().parents[2] / (
    "data/raw/CACD_2009/archive/IRBR_HIST_DO_BRASIL_3a_fase_1a_etapa.pdf"
)
with pymupdf.open(pdf) as doc:
    for pno, pg in enumerate(doc, 1):
        native = pg.get_text("text")
        has_q = "QUEST" in native.upper()
        has_rasc = "RASCUNHO" in native.upper()
        if has_q and not has_rasc:
            print(
                f"pg{pno}: native {len(native)} chars, tem QUESTAO, sem rascunho -> nativo"
            )
        else:
            txt = pytesseract.image_to_string(
                Image.open(io.BytesIO(pg.get_pixmap(dpi=250).tobytes("png"))),
                lang="por",
            )
            has_q2 = "QUEST" in txt.upper()
            has_r2 = "RASCUNHO" in txt.upper()
            print(
                f"pg{pno}: native {len(native)} | OCR {len(txt)} | QUEST={has_q2} RASCUNHO={has_r2}"
            )
