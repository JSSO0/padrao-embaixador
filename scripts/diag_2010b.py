"""2010 PARTE_I: primeiras 1500 chars e padrao das questoes."""

from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data/raw/CACD_2010/archive/IRBR_PARTE_I_2010_CAD_A_manha.pdf"
with pymupdf.open(p) as doc:
    full = "\n".join(pg.get_text("text") for pg in doc)
print(full[:1500])
print()
print("=== linhas que sao apenas numeros (11 encontradas) ===")
import re

for m in re.finditer(r"^\s*(\d{1,2})\s*$", full, re.M):
    print("   numero:", m.group(1), "| pos:", m.start())
