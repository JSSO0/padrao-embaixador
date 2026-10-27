"""Etapa 6 — Validação manual: extrai 50 questões aleatórias da 1ª fase
formatadas como markdown para conferência humana."""

import random

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
m = df[df.stage.eq("primeira_fase")].copy()
m["qn_key"] = m.contest_id + "|" + m.question_number.astype(str)

random.seed(2026)
all_keys = m["qn_key"].unique().tolist()
random.shuffle(all_keys)
selected = all_keys[:50]

out_lines = ["# Etapa 6 — Validação Manual (50 questões aleatórias)\n"]
out_lines.append(f"Amostra: 50 de {m['qn_key'].nunique()} questões da 1ª fase.\n")
out_lines.append("Marque: ✅ OK · ❌ PROBLEMA · ⚠️ DÚVIDA\n")
out_lines.append("---\n")

for qk in selected:
    sub = m[m.qn_key.eq(qk)].sort_values("item_number")
    if sub.empty:
        continue
    r = sub.iloc[0]
    out_lines.append(
        f"\n## {r['contest_id']} · Questão {int(float(r['question_number']))}"
    )
    out_lines.append(f"- **Ano:** {int(r['year'])}")
    out_lines.append(f"- **Disciplina:** {r['discipline_canon'] or '?'}")
    out_lines.append(f"- **Método:** {r['extraction_method']}")
    out_lines.append(f"- **Fonte:** `{r['source_file']}`")
    out_lines.append(f"- **Nº de itens:** {len(sub)}")

    # gabarito
    if r.get("answer") and str(r["answer"]).strip():
        out_lines.append(f"- **Gabarito:** `{r['answer']}`")
    else:
        anulada = "anulado" in str(r.get("notes") or "")
        if anulada:
            out_lines.append("- **Gabarito:** ANULADO pela banca")
        else:
            out_lines.append("- **Gabarito:** SEM RESPOSTA")

    # conteúdo
    qt = str(r["question_text"])[:200]
    out_lines.append(f"\n**Enunciado (primeiro item):**\n> {qt}\n")

    # itens
    for _, item in sub.sort_values("item_number").iterrows():
        itn = int(float(item["item_number"])) if pd.notna(item["item_number"]) else 1
        it = str(item["item_text"])[:150] if pd.notna(item["item_text"]) else ""
        if not it or it == "nan":
            it = str(item["question_text"])[:150]
        out_lines.append(
            f"- **Item {itn}:** {it} → `{item['answer'] if pd.notna(item['answer']) else '—'}`"
        )

    out_lines.append("\n**Marque:** [ ] OK  [ ] PROBLEMA\n")
    out_lines.append("---\n")

out = ROOT / "data/processed/qa_sample/qa_validacao_manual.md"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(out_lines), encoding="utf-8")
print(f"[ok] {len(selected)} questões -> {out}")
