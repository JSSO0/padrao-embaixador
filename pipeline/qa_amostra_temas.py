# -*- coding: utf-8 -*-
"""M2.5 (D1): extrai 50 itens aleatorios da 1a fase com o tema atribuido para
validacao manual da taxonomia (>= 90% de concordancia).

Cada registro traz: contest/ano, disciplina canonica, tema atribuido, se veio
de keyword ou fallback, texto do item e inicio do enunciado. A revisao julga
se o tema faz sentido para o conteudo do item.
Gera: data/processed/qa_sample/validacao_temas_m2.md (seed fixa 2028).
Uso: python pipeline/qa_amostra_temas.py [--seed 2027] [--n 50]
"""

import argparse
import random
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]

ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int, default=2028)
ap.add_argument("--n", type=int, default=50)
args = ap.parse_args()

tax = yaml.safe_load(
    (ROOT / "data/metadata/taxonomia.yaml").read_text(encoding="utf-8")
)["taxonomia"]
df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
d = df[df.stage.eq("primeira_fase")].copy()
d["qn_key"] = (
    d.contest_id + "|" + d.year.astype(str) + "|" + d.question_number.astype(str)
)

random.seed(args.seed)
idx_sample = random.sample(sorted(d.index.tolist()), args.n)

linhas = [
    "# M2.5 — Validação manual da taxonomia (50 itens)",
    "",
    f"Seed: {args.seed} · {args.n} itens de {len(d):,} da 1ª fase · taxonomia v{tax['version']} (regras fixas) · gerado em 28/10/2026".replace(
        ",", "."
    ),
    "",
    "Para cada item: leia o texto e julgue se o **tema atribuído** é o mais adequado",
    "dentro da disciplina. Marque: [x] OK · [x] Tema errado (indique o tema correto)",
    "",
    "---",
    "",
]
n_fallback = 0
for i in idx_sample:
    r = d.loc[i]
    texto = str(r["question_text"]) + " " + str(r["item_text"] or "")
    tema, matched = None, None
    # reusa a logica do classify para indicar a origem (keyword vs fallback)
    temas = tax["disciplinas"].get(r["discipline_canon"], {})
    lower = texto.lower()
    best, best_score = None, 0
    for tema_k, info in temas.items():
        score = sum(1 for kw in info["keywords"] if kw.lower() in lower)
        if score > best_score:
            best, best_score = tema_k, score
    matched = best is not None
    n_fallback += int(not matched)
    origem = (
        f"keyword `{best}` (score {best_score})"
        if matched
        else f"FALLBACK ({tax['fallback'][r['discipline_canon']]})"
    )
    itn = int(r["item_number"]) if pd.notna(r["item_number"]) else None
    qt = str(r["question_text"])[:220]
    it = str(r["item_text"])[:260] if pd.notna(r["item_text"]) else ""
    linhas.append(
        f"## {r['contest_id']} · Q{int(r['question_number'])}{'' if itn is None else f' · item {itn}'}"
    )
    linhas.append(
        f"- **Disciplina:** {r['discipline_canon']} · **Ano:** {int(r['year'])}"
    )
    linhas.append(
        f"- **Tema atribuído:** `{r['topic']}` ({'por keyword' if matched else 'fallback'})"
    )
    if matched:
        linhas.append(f"- **Keyword(s) que casaram:** `{best}`")
    linhas.append(f"- **Enunciado (início):** {qt}")
    if it != "nan":
        linhas.append(f"- **Texto do item:** {it}")
    linhas.append("")
    linhas.append("**Marque:** [ ] OK  [ ] Tema errado → correto: ______")
    linhas.append("")
    linhas.append("---")
    linhas.append("")

out = ROOT / "data/processed/qa_sample/validacao_temas_m2.md"
out.write_text("\n".join(linhas), encoding="utf-8")
print(f"[ok] {args.n} itens (seed {args.seed}) -> {out}")
print(f"     fallback na amostra: {n_fallback}")
