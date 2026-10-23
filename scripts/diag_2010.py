"""2010 PARTE_I: como as questoes sao marcadas? Onde estao q37/q38/q39/q40?"""

import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data/raw/CACD_2010/archive/IRBR_PARTE_I_2010_CAD_A_manha.pdf"
with pymupdf.open(p) as doc:
    full = "".join(pg.get_text("text") for pg in doc)

print("tamanho:", len(full), "| paginas:", len(pymupdf.open(p)))
# padroes de marcador
for pat in (r"QUEST[ÃA]O", r"Quest[ãa]o", r"^\s*\d{1,2}\s*$", r"Texto"):
    ms = re.findall(pat, full, re.M)
    print(f"  {pat!r}: {len(ms)}")
# contexto de 'julgue' e 'assinale' (os comandos das questoes)
for m in list(re.finditer(r"[Jj]ulgue|[Aa]ssinale", full))[:12]:
    idx = m.start()
    back = " ".join(full[max(0, idx - 100) : idx].split())[-70:]
    fwd = " ".join(full[idx : idx + 80].split())[:70]
    print(f"   [{back!r}] >> [{fwd!r}]")
