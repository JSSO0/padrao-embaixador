# -*- coding: utf-8 -*-
"""Resgata chaves de gabarito que o parser perdeu por agrupamento de linha
(M1.6/D1): re-parseia os PDFs com tolerancia de y maior (8pt) e adiciona ao
cache APENAS chaves ausentes (nunca sobrescreve as existentes).

Anos cobertos: 2010 (q9), 2011 (q41) — linhas duplicadas/quebradas no PDF.
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

import pymupdf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "processed" / "gabaritos.json"
RE_HEADER = re.compile(r"Quest\S{0,2}O\s*(\d{1,3})", re.I)
RE_ANS = re.compile(r"^[A-Ea-eXx#$☼]$")
TOL = 8.0  # o parser original usa 3.0 — linhas irregulares perdem letras

FILES = {
    2010: ["cursocacd/gabarito__81a90c50.pdf"],
    2011: ["archive/Gabarito.pdf", "cursocacd/gabarito__b57290a0.pdf"],
}

cache = json.loads((ROOT / "data/processed/gabaritos.json").read_text(encoding="utf-8"))


def rows_of(page, tol=TOL):
    spans = []
    seen = set()
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = unicodedata.normalize("NFC", s["text"].strip())
                if not t:
                    continue
                key = (round(s["bbox"][1], 1), round(s["bbox"][0], 1), t)
                if key in seen:
                    continue  # span duplicado no text layer
                seen.add(key)
                spans.append((s["bbox"][1], s["bbox"][0], t))
    spans.sort()
    rows = []
    for y, x, t in spans:
        if rows and abs(rows[-1][0] - y) <= tol:
            rows[-1][1].append((x, t))
        else:
            rows.append([y, [(x, t)]])
    return [sorted(c) for _, c in rows]


def parse(doc):
    out = {}
    for page in doc:
        for cells in rows_of(page):
            texts = [t for _, t in cells]
            first = texts[0].strip()
            me = RE_HEADER.fullmatch(first) or re.fullmatch(r"(\d{1,3})", first)
            if me and len(cells) >= 2:
                qn = int(me.group(1))
                # colapsa letras duplicadas na mesma coluna (span duplo do PDF)
                by_x = {}
                for x, t in cells[1:]:
                    if RE_ANS.match(t):
                        by_x.setdefault(round(x, 1), t.upper())
                lets = [v for _, v in sorted(by_x.items())]
                if lets and 1 <= qn <= 300 and len(lets) <= 6:
                    for pos, ll in enumerate(lets, 1):
                        out.setdefault((qn, pos), ll)
    return out


for year, files in FILES.items():
    g = cache.setdefault(str(year), {})
    for rel in files:
        pdf = ROOT / "data/raw" / f"CACD_{year}" / rel
        doc = pymupdf.open(pdf)
        full = " ".join(p.get_text("text") for p in doc)
        if re.search(r"\bTPS\b|PR[ÉE]-SELE[ÇC][ÃA]O", full):
            continue  # tabelas TPS: parser proprio
        got = parse(doc)
        novos = 0
        for (qn, itn), letra in sorted(got.items()):
            k = f"{qn}:{itn}"
            if k not in g:
                g[k] = letra
                novos += 1
                print(f"novo {year} {k}={letra}")
    print(f"{year}: cache agora tem {len(g)} chaves")
