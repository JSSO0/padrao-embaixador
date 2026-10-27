"""OCR dos gabaritos 2005-2013 para recuperar letras perdidas.

Roda tesseract a 300dpi (lang=por) sobre cada pagina e salva o texto para
inspecao e para reintegracao ao cache de gabaritos.
"""

import io
import os
import re
from pathlib import Path

import pymupdf

os.environ["TESSDATA_PREFIX"] = str(Path(os.environ["LOCALAPPDATA"]) / "tessdata")
os.environ["PATH"] += r";C:\Program Files\Tesseract-OCR"
import pytesseract  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

GABS = {
    2005: "data/raw/CACD_2005/cursocacd/gabarito__4031719e.pdf",
    2006: "data/raw/CACD_2006/cursocacd/gabarito__e6a8a527.pdf",
    2007: "data/raw/CACD_2007/cursocacd/gabarito__75091131.pdf",
    2009: "data/raw/CACD_2009/cursocacd/gabarito__26c6a7a3.pdf",
    2010: "data/raw/CACD_2010/cursocacd/gabarito__81a90c50.pdf",
    2012: "data/raw/CACD_2012/cursocacd/gabarito__e76b1501.pdf",
}

if __name__ == "__main__":
    for y, rel in GABS.items():
        pdf = ROOT / rel
        if not pdf.exists():
            print(f"[!!] {y}: {pdf.name} nao existe")
            continue
        # conta quantos itens com answer=null existem nesse ano
        import pandas as pd

        df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
        sub = df[(df.contest_id == f"CACD_{y}") & (df.stage == "primeira_fase")]
        sem = len(sub) - int(
            (sub.answer.notna() & sub.answer.astype(str).str.strip().ne("")).sum()
        )
        print(f"== {y} ({sub.shape[0]} itens, {sem} sem gabarito) ==")
        full = []
        with pymupdf.open(pdf) as doc:
            print(
                f"   {len(doc)} paginas | texto nativo:",
                sum(len(pg.get_text("text")) for pg in doc),
                "chars",
            )
            for pg in doc:
                pix = pg.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                txt = pytesseract.image_to_string(img, lang="por", config="--psm 6")
                full.append(txt)
        ocr = "\n".join(full)
        out = pdf.parent / f"ocr_{pdf.stem}.md"
        out.write_text(ocr, encoding="utf-8")
        print(f"   OCR salvo: {out.name} ({len(ocr)} chars)")
