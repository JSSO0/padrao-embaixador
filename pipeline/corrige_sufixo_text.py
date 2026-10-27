# -*- coding: utf-8 -*-
"""Corrige o sufixo espurio 'Text X' colado no fim de item_text (M1.7).

Defeito: em 2016/2017/2018 (transcricoes cursocacd), o cabecalho do proximo
texto ficou colado no fim do item_text do ultimo item de algumas questoes.
Corrige o JSONL fonte e as linhas correspondentes do parquet.
"""

import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RE = re.compile(r"^(.*?)(?:\s*Text\s+[IVX]+)\s*$", re.S)

# 1) JSONL fontes
jsonl_fixes = 0
for f in sorted(ROOT.glob("data/raw/CACD_20*/cursocacd/cacd_*_prova_objetiva_*.jsonl")):
    lines = f.read_text(encoding="utf-8").splitlines()
    changed = False
    for i, l in enumerate(lines):
        o = json.loads(l)
        it = (o.get("item_text") or "").strip()
        m = RE.match(it)
        if m:
            novo = m.group(1).rstrip()
            print(
                f"jsonl {f.name} q{o['question_number']} it{o['item_number']}: ...{it[-50:]!r} -> ...{novo[-40:]!r}"
            )
            o["item_text"] = novo
            lines[i] = json.dumps(o, ensure_ascii=False)
            changed = True
    if changed:
        f.write_text("\n".join(lines) + "\n", encoding="utf-8")
        jsonl_fixes += 1
print(f"arquivos jsonl corrigidos: {jsonl_fixes}")

# 2) parquet
pf = ROOT / "data/processed/questions.parquet"
df = pd.read_parquet(pf)
fixed = 0
for idx in df.index:
    it = df.at[idx, "item_text"]
    if pd.isna(it):
        continue
    mm = RE.match(str(it).strip())
    if mm:
        df.at[idx, "item_text"] = mm.group(1).rstrip()
        fixed += 1
df.to_parquet(pf, index=False)
print(f"linhas do parquet corrigidas: {fixed}")
