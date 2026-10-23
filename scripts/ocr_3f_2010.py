"""OCR 2010: provas escritas por disciplina (texto em cipher de glifos)."""

import io
import json
import os
import re
from pathlib import Path

import pymupdf

os.environ["TESSDATA_PREFIX"] = str(Path(os.environ["LOCALAPPDATA"]) / "tessdata")
os.environ["PATH"] += r";C:\Program Files\Tesseract-OCR"
import pytesseract  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SUBJ = [
    ("DIREITO_INTERNACIONAL_PUBLICO", "Direito"),
    ("ECONOMIA", "Economia"),
    ("GEOGRAFIA", "Geografia"),
    ("HISTORIA DO BRASIL", "História do Brasil"),
    ("POLIT_INTERNAC", "Política Internacional"),
]
RE_Q = re.compile(r"QUEST[ÃA]O\s+(\d{1,2})", re.I)

out_lines = []
for stem, disc in SUBJ:
    pdf = ROOT / "data/raw/CACD_2010/archive" / f"IRBR_{stem}.pdf"
    if not pdf.exists():
        print(f"[!!] {pdf.name} nao existe")
        continue
    with pymupdf.open(pdf) as doc:
        full = []
        for pno, pg in enumerate(doc, 1):
            pix = pg.get_pixmap(dpi=250)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            txt = pytesseract.image_to_string(img, lang="por")
            full.append(txt)
    body = "\n".join(full)
    qs = list(re.finditer(r"QUEST[ÃA]O\s+(\d{1,2})", body, re.I))
    print(f"[ok] {stem}: {len(qs)} questoes OCR | paginas: {len(body.split(chr(12)))}")
    # emite registros
    recs = []
    for idx, m in enumerate(qs):
        qn = int(m.group(1))
        end = qs[idx + 1].start() if idx + 1 < len(qs) else len(body)
        text = " ".join(body[m.start() : end].replace("\n", " ").split())
        if len(text) < 60:
            continue
        is_essay = bool(
            re.search(r"Extens[ãa]o m[áa]xima|valor da quest[ãa]o", text, re.I)
        )
        recs.append(
            {
                "contest_id": "CACD_2010",
                "year": 2010,
                "phase": 3,
                "stage": "terceira_fase",
                "discipline": disc,
                "question_number": qn,
                "item_number": None,
                "question_type": "essay" if is_essay else "certo_errado",
                "question_text": text,
                "item_text": None,
                "alternatives": None,
                "answer": None,
                "page": None,
                "caderno": "A",
                "source_file": f"data/raw/CACD_2010/archive/IRBR_{stem}.pdf",
                "source_url": None,
                "confidence": 0.6,
                "notes": "OCR (tesseract 5.4, por) — fonte em cipher de glifos",
            }
        )
    fname = ROOT / "data/raw/CACD_2010/archive" / f"discursivas_ocr_{stem}.jsonl"
    with fname.open("w", encoding="utf-8") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"   -> {fname.name}: {len(recs)} registros")

total = 0
for stem in (
    "DIREITO_INTERNACIONAL_PUBLICO",
    "ECONOMIA",
    "GEOGRAFIA",
    "HISTORIA DO BRASIL",
    "POLIT_INTERNAC",
):
    f = ROOT / "data/raw/CACD_2010/archive" / f"discursivas_ocr_{stem}.jsonl"
    if f.exists():
        total += len(f.open(encoding="utf-8").readlines())
print(f"[total] {total} registros de 3a fase 2010 via OCR")
