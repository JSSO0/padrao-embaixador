"""Estrutura interna: bloco da 3a fase 2013 (Direito Q1-2) e EspFra 2015 (Q1-2)."""

import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
RE_Q = re.compile(r"QUEST.{0,3}O\s*(\d{1,2})", re.I)


def block(pdf, q_from, q_to, contains=None):
    with pymupdf.open(pdf) as doc:
        full = "\n".join(pg.get_text("text") for pg in doc)
    ms = sorted((m.start(), int(m.group(1))) for m in RE_Q.finditer(full))
    s0 = next(s for s, n in ms if n == q_from)
    ends = [s for s, n in ms if s > s0 and n == q_to]
    return full[s0 : (ends[0] if ends else len(full))]


p = ROOT / "data/raw/CACD_2013/wayback/prova_discursiva__ec3e2894.pdf"
if not p.exists():
    p = Path(
        glob.glob(
            str(ROOT / "data/raw/CACD_2013/**/prova_discursiva__ec3e2894.pdf"),
            recursive=True,
        )[0]
    )
print("=== 2013 Direito: QUESTÃO 1 -> 2 ===")
print(block(p, 1, 2)[:1300])

print()
print("=== 2015 EspFra: QUESTAO 1 -> 2 ===")
p15 = ROOT / "data/raw/CACD_2015/wayback/prova_discursiva__294ac878.pdf"
if not p15.exists():
    import glob as g

    p15 = Path(
        g.glob(
            str(ROOT / "data/raw/CACD_2015/**/prova_discursiva__294ac878.pdf"),
            recursive=True,
        )[0]
    )
b = block(p15, 1, 2)
print(b[:1200])
