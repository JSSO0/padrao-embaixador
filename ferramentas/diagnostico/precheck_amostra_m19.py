# -*- coding: utf-8 -*-
"""Pre-checagem automatica da amostra M1.9: o texto de cada item transcrito
aparece no texto extraido do PDF fonte? (nao substitui a revisao manual)."""

import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", str(s)).lower()
    s = re.sub(r"[^a-z0-9áéíóúâêôãõàçü]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
m = df[df.stage.eq("primeira_fase")].copy()
m["qn_key"] = m.contest_id + "|" + m.question_number.astype(str)

# recupera as 50 da amostra gerada
md = (ROOT / "data/processed/qa_sample/qa_validacao_manual_m1.md").read_text(
    encoding="utf-8"
)
pares = re.findall(r"## (CACD_\d+) · Questão (\d+)", md)
print(f"questoes na amostra: {len(pares)}")

_cache = {}


def texto_fonte(src: str) -> str:
    if src in _cache:
        return _cache[src]
    p = ROOT / str(src).replace("data/raw/", "data/processed/text/").replace(
        ".pdf", ".txt"
    )
    t = p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""
    _cache[src] = norm(t)
    return _cache[src]


falhas = []
for contest, qn in pares:
    qn_i = int(qn)
    sub = df[
        (df.stage.eq("primeira_fase"))
        & (df.contest_id.eq(contest))
        & (df.question_number.eq(qn_i))
    ]
    src = sub.iloc[0]["source_file"]
    ftxt = texto_fonte(src)
    if not ftxt:
        falhas.append((contest, qn, "texto do PDF nao encontrado"))
        continue
    ok_q = 0
    for _, r in sub.iterrows():
        alvo = (
            norm(r["item_text"])
            if pd.notna(r["item_text"])
            else norm(r["question_text"])
        )
        # compara um recorte central do item (evita cabecalhos truncados)
        meio = alvo[20:110].strip()
        if not meio or meio in ftxt:
            ok_q += 1
    if ok_q < len(sub):
        falhas.append((contest, qn, f"{ok_q}/{len(sub)} itens conferem com o PDF"))

print(f"\nItens com desvio aparente: {len(falhas)}")
for c, q, d in falhas:
    print(
        f"  {c} q{q}: {q if False else q} {c and ''}{q} -> {d}"
        if False
        else f"  {c} q{q}: {d}"
    )
