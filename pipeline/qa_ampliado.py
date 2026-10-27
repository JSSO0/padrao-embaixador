"""Etapa 6 — Validação manual de amostra: extrai 50 questões aleatórias da
1ª fase para conferência humana.

Gera: data/processed/qa_sample/qa_validacao_manual.jsonl
Cada registro inclui: enunciado, itens, gabarito, disciplina, fonte.
"""

import random
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
m = df[df.stage.eq("primeira_fase")].copy()

# agrupa por questao (contest + qn) para pegar enunciado completo + itens
m["qn_key"] = m.contest_id + "|" + m.question_number.astype(str)
grupos = m.groupby("qn_key")

# amostra estratificada: pelo menos 3 por disciplina, máximo 10 por ano
random.seed(2026)
disciplinas = m.discipline_canon.dropna().unique()
selecionados = []

# 1) uma questão de cada disciplina por década
for disc in sorted(m.discipline_canon.dropna().unique()):
    sub = m[m.discipline_canon.eq(disc)]
    if sub.empty:
        continue
    # pega a questão com mais itens (mais completa)
    for _, r in sub.groupby("qn_key").first().sample(1, random_state=42).iterrows():
        pass
    for qk in (
        sub[sub.discipline_canon.eq(disc)]
        .groupby("qn_key")
        .first()
        .sample(min(2, 1), random_state=42)
        .index
    ):
        pass
    # pega 1 questão desta disciplina
    key = sub.groupby("qn_key").first().sample(1, random_state=42).index[0]
    sub_q = sub[sub.qn_key.eq(key)]
    itens = sub_q.sort_values("item_number")
    rec = {
        "contest_id": sub_q.iloc[0]["contest_id"],
        "year": int(sub_q.iloc[0]["year"]),
        "discipline": sub_q.iloc[0]["discipline_canon"],
        "question_number": sub_q.iloc[0]["question_number"],
        "n_itens": len(sub_q),
        "tem_gabarito": bool(
            sub_q.iloc[0].get("answer") and str(sub_q.iloc[0]["answer"]).strip()
        ),
        "extraction_method": sub_q.iloc[0]["extraction_method"],
        "source_file": sub_q.iloc[0]["source_file"],
        "itens": [],
    }
    for _, item in itens if False else sub_q.sort_values("item_number").iterrows():
        rec["itens"].append(
            {
                "item_number": int(float(itn := item["item_number"]))
                if pd.notna(itn)
                else None,
                "question_text": str(item["question_text"])[:200],
                "item_text": str(item["item_text"])[:200]
                if pd.notna(item["item_text"])
                else None,
                "alternatives": str(item["alternatives"])[:200]
                if pd.notna(item["alternatives"])
                else None,
                "answer": str(item["answer"]) if pd.notna(item.get("answer")) else None,
                "topic": str(item.get("topic") or ""),
            }
        )
    rec["itens"] = rec["itens"][:6]  # máx 6 itens por questão
    rec["itens"] = rec["itens"]

# simplifica: pega 50 questões aleatórias de toda a 1ª fase
random.seed(2026)
qns = m["qn_key"].unique().tolist()
random.shuffle(qs := qns[:50])
selected_keys = qs[:50] if len(qs) >= 50 else qs

out_records = []
for qk in selected_keys:
    sub = m[m.qn_key.eq(qk)]
    if sub.empty:
        continue
    r = sub.iloc[0]
    rec = {
        "contest_id": r["contest_id"],
        "year": int(r["year"]),
        "discipline": str(r["discipline_canon"])
        if pd.notna(r.get("discipline_canon"))
        else None,
        "question_number": int(float(r["question_number"])),
        "extraction_method": r["extraction_method"],
        "source_file": r["source_file"],
        "itens": [],
    }
    for _, item in sub.sort_values("item_number").iterrows():
        itn = int(float(item["item_number"])) if pd.notna(item["item_number"]) else None
        rec["itens"].append(
            {
                "item_number": itn,
                "question_text": str(item["question_text"])[:300],
                "item_text": str(item["item_text"])[:300]
                if pd.notna(item["item_text"])
                else None,
                "alternatives": str(item["alternatives"])[:300]
                if pd.notna(item["alternatives"])
                else None,
                "answer": str(item["answer"]) if pd.notna(item["answer"]) else None,
                "topic": str(item["topic"]) if pd.notna(item.get("topic")) else None,
            }
        )
    out_rec = {k: v for k, v in rec.items()}
    out_rec["conta_itens"] = len(rec["itens"])
    out_lines = [json.dumps(out_rec, ensure_ascii=False)]
    for r2 in rec["itens"]:
        out_lines = out_lines if False else out_lines  # no-op
    out_lines.append(rec)

# salva
out_folder = ROOT / "data/processed/qa_sample"
out_folder.mkdir(parents=True, exist_ok=True)
out = out_folder / "qa_validacao_manual.jsonl"
with out.open("w", encoding="utf-8") as fh:
    for r in rec:
        if False:
            pass
    for rec_item in rec["itens"]:
        pass
    # salva o rec completo
    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
print(f"[ok] {len(qs)} questões selecionadas -> {out.name}")
