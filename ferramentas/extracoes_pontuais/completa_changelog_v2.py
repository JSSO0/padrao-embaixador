# -*- coding: utf-8 -*-
"""Completa o changelog v2 com as 20 fusoes do M2.4."""

import sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
YAML_PATH = Path(__file__).resolve().parents[2] / "data/metadata/taxonomia.yaml"

doc = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
tax = doc["taxonomia"]

MERGES = {
    "Língua Portuguesa/estilo_registro": "semântica (registro e uso da língua)",
    "Língua Portuguesa/tradução": "reescrita (versão/transposição)",
    "Língua Inglesa/summary_essay": "reading_comprehension (produção escrita)",
    "Língua Inglesa/translation": "reading_comprehension (compreensão para traduzir)",
    "Língua Inglesa/textual_analysis": "grammar_semantics (coesão/referência)",
    "História do Brasil/período_regencial": "império (fase do Primeiro Reinado)",
    "História do Brasil/nova_república": "era_militar (regime e transição)",
    "História do Brasil/economia_brasileira": "era_vargas (desenvolvimentismo)",
    "História Mundial/revolução_russa": "guerra_fria (socialismo/bipolaridade)",
    "História Mundial/revolução_mexicana": "revoluções_liberais (movimento revolucionário)",
    "História Mundial/globalização": "revolução_industrial (mundialização do capitalismo)",
    "História Mundial/doutrinas_e_teorias": "revoluções_liberais (doutrinas liberais)",
    "Geografia/economia_regional": "urbanização (desenvolvimento regional)",
    "Política Internacional/doutrinas": "multilateralismo (pan-americanismo)",
    "Política Internacional/teorias_RI": "segurança_internacional (securitização)",
    "Economia/finanças_públicas": "macroeconomia (política fiscal)",
    "Economia/monetário": "macroeconomia (moeda e política monetária)",
    "Direito/direito_administrativo": "organização_do_estado (administração pública)",
    "Direito/mercosul_direito": "internacional_público (bloco regional)",
    "Economia/economia_internacional": "comércio_internacional (fluxos globais)",
}

tax["changelog"] = [
    {
        "versao": 1,
        "data": "2026-10-28",
        "mudanca": "Taxonomia criada a partir das regras refinadas (60 temas + Cultura Geral)",
    },
    {
        "versao": 2,
        "data": "2026-10-28",
        "mudanca": (
            "M2.4: temas com < 0,5% dos itens fundidos em temas semanticamente "
            "adjacentes. Resultado: 40 temas, max 7,36%, min 0,56%."
        ),
        "merges": MERGES,
    },
]

YAML_PATH.write_text(
    yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100),
    encoding="utf-8",
)
print(f"changelog v2: {len(MERGES)} merges registrados")
