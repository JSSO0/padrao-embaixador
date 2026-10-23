"""Mini-inventario 2013-2016 (wayback): prova, fase declarada, disciplina, marcadores."""

import glob
import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
RE_Q = re.compile(r"QUEST.{0,3}O\s*(\d{1,2})", re.I)
RE_FASE = re.compile(r"(PRIMEIRA|SEGUNDA|TERCEIRA)\s+FASE", re.I)
RE_PROVA = re.compile(r"PROVA\s+DE\s+([A-ZÀ-Ú ]{3,60})", re.I)
RE_ESCRITA = re.compile(r"PROVA\s+ESCRITA\s+DE\s+([A-ZÀ-Ú ]{3,60})", re.I)

for y in (2013, 2014, 2015, 2016):
    fs = sorted(
        glob.glob(f"data/raw/CACD_{y}/**/prova_discursiva*.pdf", recursive=True)
    ) + sorted(glob.glob(f"data/raw/CACD_{y}/**/discursiva_*.pdf", recursive=True))
    print("=" * 20, y, f"({len(fs)} arquivos)")
    for p in fs:
        with pymupdf.open(p) as doc:
            full = "\n".join(pg.get_text("text") for pg in doc)
        fases = sorted({m.group(1) for m in RE_FASE.finditer(full)})
        prova = sorted({m.group(1).strip() for m in RE_PROVA.finditer(full)})
        escrita = sorted(
            {
                m.group(1).strip()
                for m in re.finditer(r"PROVA ESCRITA DE ([A-ZÀ-Ú ]{3,60})", full, re.I)
            }
        )
        qs = sorted({int(m.group(1)) for m in RE_Q.finditer(full)})
        # disciplinas citadas
        print(
            f"   {Path(p).name[:44]:44} | fase:{fases} | prova:{prova[:2]} | escrita:{escrita[:2]} | q: {qs[:3]}..{qs[-3:] if qs else ''} ({len(qs)})"
        )
