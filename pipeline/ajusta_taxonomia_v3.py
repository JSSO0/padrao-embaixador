# -*- coding: utf-8 -*-
"""Ajustes da validacao M2.5 (68% -> >=90%): disciplina de 2018 q43 e
afinamento de keywords do YAML v3."""

import json
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]

# --- 1) disciplina de 2018 q43 (prova: Text VI = lingua inglesa) ----------
# JSONL fonte
f = ROOT / "data/raw/CACD_2018/cursocacd/cacd_2018_primeira_fase_prova_objetiva_2.jsonl"
lines = f.read_text(encoding="utf-8").splitlines()
fix = 0
for i, l in enumerate(lines):
    o = json.loads(l)
    if o.get("question_number") == 43:
        o["discipline"] = "Língua Inglesa"
        lines[i] = json.dumps(o, ensure_ascii=False)
        fix += 1
f.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"jsonl 2018 q43: {fix} linhas corrigidas -> Língua Inglesa")

# parquet
pf = ROOT / "data/processed/questions.parquet"
df = pd.read_parquet(pf)
sel = (
    df.stage.eq("primeira_fase")
    & df.contest_id.eq("CACD_2018")
    & df.question_number.eq(43)
)
df.loc[sel, "discipline"] = "Língua Inglesa"
df.loc[sel, "discipline_canon"] = "Língua Inglesa"
print(f"parquet: {int(sel.sum())} linhas de 2018 q43 -> Língua Inglesa")

# --- 2) afinamento de keywords (YAML v3) -----------------------------------
YAML_PATH = ROOT / "data/metadata/taxonomia.yaml"
doc = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
tax = doc["taxonomia"]
discs = tax["disciplinas"]

# LP: 'pronome'/'preposição' genericas (morfologia) e semantica mais forte
morf = discs["Língua Portuguesa"]["morfologia"]["keywords"]
for k in ("pronome", "preposição"):
    if k in morf:
        morf.remove(k)
discs["Língua Portuguesa"]["semântica"]["keywords"].extend(
    ["recursos semânticos", "recursos discursivos", "discursivos", "sinônimo"]
)

# LI: 'sentence'/'paragraph' genericas na grammar_semantics
gs = discs["Língua Inglesa"]["grammar_semantics"]["keywords"]
for k in ("sentence", "paragraph"):
    if k in gs:
        gs.remove(k)

# Geo: 'ambiental' sai da fisica; urbanizacao ganha termos regionais
geo_fis = discs["Geografia"]["geografia_física"]["keywords"]
if "ambiental" in geo_fis:
    geo_fis.remove("ambiental")
discs["Geografia"]["urbanização"]["keywords"].extend(
    ["regionais", "povoamento", "industrialização"]
)
discs["Geografia"]["meio_ambiente"]["keywords"].append("governança ambiental")

# Economia: chaves especificas
discs["Economia"]["comércio_internacional"]["keywords"].extend(
    ["cambial", "fluxos externos"]
)
discs["Economia"]["desenvolvimento"]["keywords"].extend(
    ["economia brasileira", "indústrias tradicionais"]
)
discs["Economia"]["macroeconomia"]["keywords"].extend(
    ["identidades macroeconômicas", "contas nacionais"]
)
# microeconomia: remove genericos que capturam qualquer texto econômico
micro = discs["Economia"]["microeconomia"]["keywords"]
for k in ("mercado", "equilíbrio"):
    if k in micro:
        micro.remove(k)

# Direito: costumes internacionais
discs["Direito"]["internacional_público"]["keywords"].append("costumes internacionais")

# Historia Mundial: revolucoes_liberais recupera os casos do seculo XIX
discs["História Mundial"]["revoluções_liberais"]["keywords"].extend(
    [
        "movimentos revolucionários",
        "proclamação do império alemão",
        "unificação alemã",
        "independência",
    ]
)

tax["version"] = 3
tax["changelog"].append(
    {
        "versao": 3,
        "data": "2026-10-28",
        "mudanca": (
            "M2.5 (1a validacao: 34/50 = 68%): afinamento de keywords "
            "(removidos termos genericos de grammar_semantics e morfologia; "
            "novas chaves em semantica, comercio_internacional, "
            "desenvolvimento, macroeconomia, urbanizacao, meio_ambiente, "
            "internacional_publico e revoluciones_liberais) e correcao da "
            "disciplina de 2018 q43 (Text VI = Língua Inglesa)."
        ),
    }
)

YAML_PATH.write_text(
    yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100),
    encoding="utf-8",
)
print("yaml: v3 salvo")

# --- 3) reclassifica -------------------------------------------------------
sys.path.insert(0, str(ROOT))
from pipeline.build_taxonomy import classify, carregar_taxonomia  # noqa: E402

tax = carregar_taxonomia()
n_fb = 0
for idx in df.index[df.stage.eq("primeira_fase")]:
    dd = df.at[idx, "discipline_canon"]
    if pd.isna(dd) or dd not in tax["disciplinas"]:
        continue
    texto = str(df.at[idx, "question_text"]) + " " + str(df.at[idx, "item_text"] or "")
    tema, matched = classify(texto, dd, tax)
    n_fb += int(not matched)
    df.at[idx, "topic"] = tema
df.to_parquet(pf, index=False)
print(f"reclassificado | fallback: {n_fb}")
