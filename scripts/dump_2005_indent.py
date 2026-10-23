"""Dump com x0 das linhas dos blocos 2005 (q9-11) + procura q38-39 no 2010."""

import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]

p = ROOT / "data/raw/CACD_2005/archive/CESPE-2005-IRBR-Diplomata.pdf"
with pymupdf.open(p) as doc:
    full = "".join(pg.get_text("text") for pg in doc)
RE_MARK = re.compile(r"QUEST.{0,3}O\s*(\d{1,3})", re.I)
marks = sorted((m.start(), int(m.group(1))) for m in RE_MARK.finditer(full))
m0 = next(s for s, n in marks if n == 9)
m1 = next(s for s, n in marks if n == 10)
# pega a pagina e o dict
with pymupdf.open(p) as doc:
    for pno, pg in enumerate(doc, 1):
        t = pg.get_text("text")
        if "QUESTÃO 9" in t:
            # linhas com x0
            for b in pg.get_text("dict")["blocks"]:
                for l in b.get("lines", []):
                    for s in l["spans"]:
                        if s["text"].strip():
                            x0 = round(s["bbox"][0])
                            print(f"x={x0:3} | {s['text'].strip()[:80]}")
            break
print()
print("=== 2010: marcadores no PARTE_I perto de 37-40 ===")
p10 = ROOT / "data/raw/CACD_2010/archive/IRBR_PARTE_I_2010_CAD_A_manha.pdf"
with pymupdf.open(p10) as doc:
    full10 = "".join(pg.get_text("text") for pg in doc)
idx = full10.find("37")
print(repr(full10[idx - 200 : idx + 400]))
