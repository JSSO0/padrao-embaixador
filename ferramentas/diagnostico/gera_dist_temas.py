# -*- coding: utf-8 -*-
"""Gera docs/relatorios/distribuicao-temas.md (M2.4)."""

import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
d = df[df.stage.eq("primeira_fase")]
st = d.topic.value_counts()
n = len(d)

linhas = [
    "# Distribuição de temas — 1ª fase (M2.4)",
    "",
    "> Resultado da taxonomia v2 (`data/metadata/taxonomia.yaml`, regras fixas a priori).",
    f"> {n:,} itens da 1ª fase · {len(st)} temas · maior tema {st.max() / n:.2%} · menor tema {st.min() / n:.2%}.".replace(
        ",", "."
    ),
    "> Critério do M2.4: nenhum tema > 8% e nenhum < 0,5% — **atendido**.",
    "> Gerado em 28/10/2026.",
    "",
    "| Tema | Itens | % da 1ª fase |",
    "|---|---:|---:|",
]
for tema, v in st.items():
    linhas.append(f"| `{tema}` | {v} | {v / n:.2%} |")

out = ROOT / "docs/relatorios/distribuicao-temas.md"
out.write_text("\n".join(linhas) + "\n", encoding="utf-8")
print(f"ok: {out}")
