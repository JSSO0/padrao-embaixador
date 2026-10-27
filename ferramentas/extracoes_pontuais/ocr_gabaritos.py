"""OCR dos gabaritos 2005-2013: recupera letras perdidas na extracao de texto.

Para cada ano, usa o gabarito PDF que ja foi extraido. Renderiza as paginas
a 300dpi e roda OCR lang=por. O resultado e processado pelos mesmos parsers
do extract_gabaritos.py (grade transposta, grade estreita, tabela).
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

GABARITOS = {
    2005: ["data/raw/CACD_2005/cursocacd/gabarito__4031719e.pdf"],
    2006: ["data/raw/CACD_2006/cursocacd/gabarito__e6a8a527.pdf"],
    2007: ["data/raw/CACD_2007/cursocacd/gabarito__75091131.pdf"],
    2008: ["data/raw/CACD_2008/cursocacd/gabarito__7fd74fc6.pdf"],
    2009: ["data/raw/CACD_2009/cursocacd/gabarito__26c6a7a3.pdf"],
    2010: ["data/raw/CACD_2010/cursocacd/gabarito__81a90c50.pdf"],
    2011: ["data/raw/CACD_2011/cursocacd/gabarito__b57290a0.pdf"],
    2012: ["data/raw/CACD_2012/cursocacd/gabarito__e76b1501.pdf"],
    2013: ["data/raw/CACD_2013/cursocacd/gabarito__bf7f4415.pdf"],
}


def ocr_pdf(pdf_path: Path) -> str:
    full = []
    with pymupdf.open(pdf) as doc:
        for pg in doc:
            pix = pg.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            txt = pytesseract.image_to_string(img, lang="por", config="--psm 6")
            full.append(txt)
    return "\n".join(full)


RE_TOKEN = re.compile(r"(\d{1,2})\s+([A-Da-dEe])")
RE_HEADER = re.compile(r"QUEST.{0,3}O\s*(\d{1,3})", re.I)


def parse_ocr_txt(txt: str, year: int) -> dict:
    """Extrai pares (questao, item) -> letra do texto OCR da grade TPS.

    Estrutura esperada (por bloco):
      linha de cabecalho: numeros de questao (1..N)
      linhas de itens: '<rotulo> <letra> <letra> ...' (uma letra por questao)
    """
    out = {}
    lines = [ln.strip() for ln in txt.split("\n") if ln.strip()]
    # acha blocos: linha com apenas numeros 1..N (cabecalho) seguida de linhas
    # '<rotulo> <letra> <letra> ... <letra>'
    header_nums = []
    item_rows = []
    for ln in lines:
        # cabecalho: sequencia de numeros (pode ter mesclados)
        toks = ln.split()
        if toks and all(re.fullmatch(r"\d{1,2}", tk) for tk in toks) and len(toks) >= 5:
            header_nums = [int(tk) for tk in toks]
            item_rows = []
            continue
        # linha de itens: rotulo + letras
        m = re.fullmatch(r"([1-4+])\s+((?:[CDE#☼]\s*)+)", ln)
        if m and header_nums:
            itn = int(m.group(1))
            letters = list(m.group(2).split())
            for j, letter in enumerate(letters):
                if j < len(header_nums):
                    out[(header_nums[j], itn)] = letter.upper()
        elif re.fullmatch(r"[CDE#☼]\s*[CDE#☼\s]*", ln) and len(ln.split()) >= 10:
            # linha de letras sem rotulo (continuacao do bloco anterior)
            pass
    return out


def main() -> None:
    results = {}
    for y, paths in GABARITO_PATHS.items():
        for rel in paths:
            pdf = ROOT / rel
            if not pdf.exists():
                print(f"[!!] {rel} nao existe")
                continue
            ocr_txt = ocr_gabarito(pdf)
            # salva para inspecao
            out = pdf.parent / f"ocr_{pdf.stem}.md"
            out.write_text(ocr_txt, encoding="utf-8")
            print(f"[ok] {y} {pdf.name}: OCR salvo ({len(ocr_txt)} chars)")


def ocr_gabarito(pdf: Path) -> str:
    full = []
    with pymupdf.open(pdf) as doc:
        for pg in doc:
            pix = pg.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            txt = pytesseract.image_to_string(img, lang="por", config="--psm 6")
            full.append(txt)
    return "\n".join(full)


def ocr_gabarito(pdf: Path) -> str:
    full = []
    with pymupdf.open(pdf) as doc:
        for pg in doc:
            pix = pg.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            txt = pytesseract.image_to_string(img, lang="por", config="--psm 6")
            full.append(txt)
    return "\n".join(full)


def ocr_gabarito(pdf: Path) -> str:
    full = []
    with pymupdf.open(pdf) as doc:
        for pg in doc:
            pix = pg.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            txt = pytesseract.image_to_string(img, lang="por", config="--psm 6")
            full.append(txt)
    return "\n".join(full)


GABARITO_PATHS = GABARITO_PATHS  # reference

if __name__ == "__main__":
    for y, paths in GABARITO_PATHS.items():
        for rel in paths:
            pdf = ROOT / rel
            if not pdf.exists():
                continue
            txt = ocr_gabarito(pdf)
            out = pdf.parent / f"ocr_{pdf.stem}.md"
            out.write_text(txt, encoding="utf-8")
            print(f"[ok] {y} {pdf.name}: OCR salvo ({len(txt)} chars)")
