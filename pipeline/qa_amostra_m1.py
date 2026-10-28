# -*- coding: utf-8 -*-
"""Etapa E2 (M1.9): extrai 50 questoes aleatorias da 1a fase (nova seed) para
validacao manual de fidelidade.

Diferencas do extract_faltantes.py (amostra antiga, 88%):
  - seed nova (2027), amostra independente
  - exibe "ANULADO pela banca" quando notes contem "anulado" (M1.5)
  - inclui a fonte (PDF) e o N de itens para conferencia contra o PDF
Gera: data/processed/qa_sample/qa_validacao_manual_m1.md (nao sobrescreve a
amostra antiga). Aceite do M1.9: >= 97% OK na revisao manual.
Uso: python pipeline/qa_amostra_m1.py [--seed 2027]
"""

import argparse
import random
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/processed/qa_sample/qa_validacao_manual_m1.md"

ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int, default=2027)
ap.add_argument("--n", type=int, default=50)
args = ap.parse_args()

df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
m = df[df.stage.eq("primeira_fase")].copy()
m["qn_key"] = m.contest_id + "|" + m.question_number.astype(str)

import random

random.seed(args.seed)
all_keys = m["qn_key"].unique().tolist()
random.shuffle(all_keys)
selected = all_keys[: args.n]

lines = [
    "# M1.9 — Validação manual de fidelidade (50 questões, nova amostra)\n",
    f"Seed: {args.seed} · 50 de {m['qn_key'].nunique()} questões da 1ª fase · gerado em 28/10/2026\n",
    "Compare cada questão com o PDF indicado em **Fonte**. Marque: ✅ OK · ❌ PROBLEMA · ⚠️ DÚVIDA\n",
    "---\n",
]

n_problemas_previos = 0
for qk in selected:
    sub = m[m.qn_key.eq(qk)].sort_values("item_number")
    if sub.empty:
        continue
    r = sub.iloc[0]
    # gabarito da questao
    if r.get("answer") and str(r["answer"]).strip():
        gab = f"`{r['answer']}`"
    elif "anulado" in str(r.get("notes") or "").lower():
        gab = "ANULADO pela banca"
        n_problemas_previos += 1
    else:
        gab = "SEM RESPOSTA"
        n_problemas_previos += 1
    lines.append(f"\n## {r['contest_id']} · Questão {int(float(r['question_number']))}")
    lines.append(f"- **Ano:** {int(r['year'])}")
    lines.append(f"- **Disciplina:** {r['discipline_canon'] or r['discipline'] or '?'}")
    lines.append(f"- **Método:** {r['extraction_method']}")
    lines.append(f"- **Fonte:** `{r['source_file']}`")
    lines.append(f"- **Nº de itens:** {len(sub)}")
    lines.append(f"- **Gabarito:** {gab}")
    qt = str(r["question_text"])[:250]
    lines.append(f"\n**Enunciado (início):**\n> {qt}\n")
    for _, item in sub.iterrows():
        itn = int(float(item["item_number"])) if pd.notna(item["item_number"]) else 1
        it = str(item["item_text"])[:180] if pd.notna(item["item_text"]) else ""
        if not it or it == "nan":
            it = str(item["question_text"])[:180]
        ans = (
            f"`{item['answer']}`"
            if pd.notna(item["answer"])
            else ("anulado" if "anulado" in str(item.get("notes") or "") else "—")
        )
        lines.append(f"- **Item {itn}:** {it} → {ans}")
    lines.append("\n**Marque:** [ ] OK  [ ] PROBLEMA\n")
    lines.append("---\n")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"[ok] {args.n} questões (seed {args.seed}) -> {OUT}")
print(
    f"     avisos previos: {n_problemas_previos} questoes com gabarito ausente/anulado na amostra"
)
