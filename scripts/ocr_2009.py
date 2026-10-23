"""OCR da 3a fase 2009 (provas escritas: corpo fora da camada de texto).

Renderiza cada pagina a 250 dpi e roda tesseract (lang=por). Teste na
pagina 3 da prova de Historia do Brasil.
"""

import io
import os
import sys
from pathlib import Path

import pymupdf

os.environ["TESSDATA_PREFIX"] = str(Path(os.environ["LOCALAPPDATA"]) / "tessdata")
os.environ["PATH"] += r";C:\Program Files\Tesseract-OCR"
import pytesseract  # noqa: E402
from PIL import Image  # noqa: E402

pdf = Path(__file__).resolve().parents[1] / (
    "data/raw/CACD_2009/archive/IRBR_HIST_DO_BRASIL_3a_fase_1a_etapa.pdf"
)
with pymupdf.open(pdf) as doc:
    print("paginas:", len(doc))
    for pno in (1, 2, 3):
        pg = doc[pno]
        pix = pg.get_pixmap(dpi=250)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        txt = pytesseract.image_to_string(img, lang="por")
        print("=" * 20, f"pagina {pno + 1}")
        n = 0
        for ln in txt.split("\n"):
            if ln.strip():
                print("   ", ln.strip()[:100])
                n += 1
                if n >= 14:
                    break
