# -*- coding: utf-8 -*-
"""Ajustes v5 da taxonomia (M2.5, 3a validacao: 38/50 = 76%).

Correcoes diretas (fallbacks sem keyword e chaves discriminantes).
Residual conhecido: ~7 itens por 50 sao ambiguidades de stem (o enunciado
compartilhado dispara o tema "errado" para itens cujo conteudo aponta para
outro tema) — inerente ao metodo de keywords.
"""

import sys
from pathlib import Path

import pandas as pd
import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "data/metadata/taxonomia.yaml"
PATH = ROOT / "data/processed/questions.parquet"

doc = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
tax = doc["taxonomia"]
discs = tax["disciplinas"]

# Direito: direito dos tratados -> internacional_publico
discs["Direito"]["internacional_público"]["keywords"].extend(
    ["direito dos tratados", "cooperação jurídica", "costumes internacionais"]
)
# HM: constitucionalismo ibérico -> revoluções_liberais
discs["História Mundial"]["revoluções_liberais"]["keywords"].append(
    "constitucionalismo"
)
# HB: barão do Rio Branco -> política_externa
discs["História do Brasil"]["política_externa"]["keywords"].extend(
    ["rio branco", "barão do rio branco"]
)
# LP: campo semântico -> semântica
discs["Língua Portuguesa"]["semântica"]["keywords"].append("campo semântico")
# LI: 'word' sai de grammar_semantics (generico; vocabulary tem 'word')
gs = discs["Língua Inglesa"]["grammar_semantics"]["keywords"]
if "word" in gs:
    gs.remove("word")
# Geo: zonas urbanas/taxas de desemprego -> urbanizacao
discs["Geografia"]["urbanização"]["keywords"].extend(
    ["zonas urbanas", "taxas de desemprego"]
)
# Eco: indústria brasileira -> desenvolvimento
discs["Economia"]["desenvolvimento"]["keywords"].append("indústria brasileira")

tax["version"] = 5
tax["changelog"].append(
    {
        "versao": 5,
        "data": "2026-10-28",
        "mudanca": (
            "M2.5 (2a validacao: 38/50 = 76%): chaves discriminantes novas "
            "(direito dos tratados, campo semantico, constitucionalismo, "
            "barao do rio branco, zonas urbanas, industria brasileira) e "
            "'word' removida de grammar_semantics."
        ),
    }
)

YAML_PATH.write_text(
    yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100),
    encoding="utf-8",
)
print("yaml: v5 salvo")

sys.path.insert(0, str(ROOT))
from pipeline.build_taxonomy import classify, carregar_taxonomia  # noqa: E402

tax = carregar_taxonomia()
df = pd.read_parquet(PATH)
n_fb = 0
for idx in df.index[df.stage.eq("primeira_fase")]:
    dd = df.at[idx, "discipline_canon"]
    if pd.isna(dd) or dd not in tax["disciplinas"]:
        continue
    texto = str(df.at[idx, "question_text"]) + " " + str(df.at[idx, "item_text"] or "")
    tema, matched = classify(texto, dd, tax)
    n_fb += int(not matched)
    df.at[idx, "topic"] = tema
df.to_parquet(PATH, index=False)
print(f"reclassificado | fallback: {n_fb}")
