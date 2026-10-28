# -*- coding: utf-8 -*-
"""M2.4 (Fase C): funde os temas com < 0,5% dos itens da 1a fase nos temas
semanticamente adjacentes, atualizando data/metadata/taxonomia.yaml e
reclassificando o parquet. Registra o changelog no YAML."""

import json
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "data/metadata/taxonomia.yaml"
PATH = ROOT / "data/processed/questions.parquet"

# (disciplina, tema raro) -> (destino, justificativa)
MERGES = {
    ("Língua Portuguesa", "estilo_registro"): (
        "semântica",
        "registro e uso da língua são semântica aplicada",
    ),
    ("Língua Portuguesa", "tradução"): (
        "reescrita",
        "versão/transposição é reescrita entre línguas",
    ),
    ("Língua Inglesa", "summary_essay"): (
        "reading_comprehension",
        "produção escrita associada à compreensão",
    ),
    ("Língua Inglesa", "translation"): (
        "reading_comprehension",
        "tradução depende da compreensão do texto",
    ),
    ("Língua Inglesa", "textual_analysis"): (
        "grammar_semantics",
        "coesão/referência são gramática em uso",
    ),
    ("História do Brasil", "período_regencial"): (
        "império",
        "regências fazem parte do Primeiro Reinado",
    ),
    ("História do Brasil", "nova_república"): (
        "era_militar",
        "regime militar e transição política",
    ),
    ("História do Brasil", "economia_brasileira"): (
        "era_vargas",
        "desenvolvimentismo e intervenção estatal",
    ),
    ("História Mundial", "revolução_russa"): (
        "guerra_fria",
        "socialismo soviético e bipolaridade",
    ),
    ("História Mundial", "revolução_mexicana"): (
        "revoluções_liberais",
        "movimento revolucionário do período",
    ),
    ("História Mundial", "globalização"): (
        "revolução_industrial",
        "mundialização do capitalismo",
    ),
    ("História Mundial", "doutrinas_e_teorias"): (
        "revoluções_liberais",
        "doutrinas liberais e teorias associadas",
    ),
    ("Geografia", "economia_regional"): (
        "urbanização",
        "desenvolvimento regional e desigualdades territoriais",
    ),
    ("Política Internacional", "doutrinas"): (
        "multilateralismo",
        "pan-americanismo e fóruns multilaterais",
    ),
    ("Política Internacional", "teorias_RI"): (
        "segurança_internacional",
        "securitização pertence aos estudos de segurança",
    ),
    ("Economia", "finanças_públicas"): (
        "macroeconomia",
        "política fiscal é parte da macroeconomia",
    ),
    ("Economia", "monetário"): (
        "macroeconomia",
        "moeda e política monetária são agregados macro",
    ),
    ("Direito", "direito_administrativo"): (
        "organização_do_estado",
        "administração pública é organização do Estado",
    ),
    ("Direito", "mercosul_direito"): (
        "internacional_público",
        "bloco regional é direito internacional",
    ),
    ("Economia", "economia_internacional"): (
        "comércio_internacional",
        "fluxos globais são parte do comércio internacional",
    ),
}

doc = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
tax = doc["taxonomia"]
disciplinas = tax["disciplinas"]

faltando = []
for (disc, tema), (destino, _) in MERGES.items():
    info = disciplinas.get(disc, {}).pop(tema, None)
    if info is None:
        faltando.append((disc, tema))
        continue
    alvo = disciplinas[disc][destino]
    alvo["keywords"] = sorted(set(alvo["keywords"] + info["keywords"]))

tax["version"] = 2
tax["changelog"] = [
    {
        "versao": 2,
        "data": "2026-10-28",
        "mudanca": "M2.4: temas com < 0,5% dos itens fundidos em temas adjacentes",
        "merges": {f"{d}/{t}": f"{v[0]} ({v[1]})" for (d, t), v in MERGES.items()},
    }
]
if faltando:
    print("[aviso] temas ausentes no YAML:", faltando)

YAML_PATH.write_text(
    yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100),
    encoding="utf-8",
)
print(f"yaml: v{tax['version']} | merges aplicados: {len(MERGES) - len(faltando)}")

# reclassifica
sys.path.insert(0, str(ROOT))
from pipeline.build_taxonomy import classify, carregar_taxonomia  # noqa: E402

tax = carregar_taxonomia()
df = pd.read_parquet(PATH)
n_fallback = 0
for idx in df.index[df.stage.eq("primeira_fase")]:
    disc = df.at[idx, "discipline_canon"]
    if pd.isna(disc) or disc not in tax["disciplinas"]:
        continue
    texto = str(df.at[idx, "question_text"]) + " " + str(df.at[idx, "item_text"] or "")
    tema, matched = classify(texto, disc, tax)
    n_fallback += int(not matched)
    df.at[idx, "topic"] = tema
df.to_parquet(PATH, index=False)
print(f"reclassificado | fallback: {n_fallback}")
