"""Viabilidade das discursivas 2003-2016: qualidade do texto em 3 amostras."""

from pathlib import Path

import glob
import pymupdf

ROOT = Path(__file__).resolve().parents[1]

CASES = [
    ("data/raw/CACD_2003/archive/Segunda_Fase_Port_Escr.pdf", "2003 (zip archive)"),
    ("data/raw/CACD_2010/archive/IRBR_ECONOMIA.pdf", "2010 (zip archive)"),
    ("data/raw/CACD_2015/wayback/prova_discursiva__294ac878.pdf", "2015 (wayback)"),
    ("data/raw/CACD_2019/secondary/discursiva_historia__*.pdf", "2019 (secundário)"),
]
for pat, tag in CASES:
    fs = glob.glob(str(ROOT / pat)) or glob.glob(
        str(ROOT / pat.replace("secondary", "*"))
    )
    if not fs:
        fs = glob.glob(
            str(ROOT / f"data/raw/CACD_2019/**/discursiva_historia*.pdf"),
            recursive=True,
        )
    if not fs:
        print("==", tag, ": arquivo nao encontrado")
        continue
    p = fs[0]
    print("=" * 25, tag, "|", Path(p).name)
    with pymupdf.open(p) as doc:
        print("   paginas:", len(doc))
        t = "".join(pg.get_text("text") for pg in doc)
        print("   chars:", len(t))
        lines = [ln.strip() for ln in t.split("\n") if ln.strip()]
        for ln in lines[:12]:
            print("     ", ln[:95])
        import re

        qs = re.findall(r"QUEST.{0,3}O\s*\d+|Quest[ãa]o\s+\d+", t)
        print("   marcadores de questao:", qs[:12])
