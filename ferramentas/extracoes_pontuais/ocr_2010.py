"""OCR do PARTE_I 2010 (texto em encoding de glifos corrompido) para achar
as questoes 38-39."""

import io
import os
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[2]
os.environ["TESSDATA_PREFIX"] = str(Path(os.environ["LOCALAPPDATA"]) / "tessdata")
os.environ["PATH"] += r";C:\Program Files\Tesseract-OCR"
import pytesseract  # noqa: E402
from PIL import Image  # noqa: E402

pdf = Path(__file__).resolve().parents[2] / (
    "data/raw/CACD_2010/archive/IRBR_PARTE_I_2010_CAD_A_manha.pdf"
)
with pymupdf.open(pdf) as doc:
    print("paginas:", len(doc))
    pages = []
    for pno, pg in enumerate(doc, 1):
        native = pg.get_text("text")
        if "QUEST" in native.upper():
            pages.append((pno, native))
            continue
        pix = pg.get_pixmap(dpi=250)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        txt = pytesseract.image_to_string(img, lang="por")
        pages.append((pno, txt))
full = "\n".join(t for _, t in pages)

# salva para inspecao
out = ROOT / "data/raw/CACD_2010/archive/ocr_parte_i_2010.md"
out.write_text(full, encoding="utf-8")
print("[ok] OCR completo salvo:", out.name, "| chars:", len(full))

# onde estao as questoes?
ms = list(re.finditer(r"QUEST[ÃA]O\s+(\d{1,2})", full, re.I))
print("marcadores:", [(int(m.group(1)), m.start()) for m in ms][:20])
