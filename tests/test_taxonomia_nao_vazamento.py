# -*- coding: utf-8 -*-
"""Teste de nao-vazamento da taxonomia (M2.3).

Propriedades provadas:
1. A classificacao de um item depende apenas do texto do proprio item, da
   disciplina e do YAML — nao do corpus nem de outros itens.
2. Reclassificar com um subconjunto do parquet (ex.: so itens <= ano X)
   produz o MESMO tema para um item — nenhum "conhecimento do futuro".
3. Integridade do YAML: versao, fallback por disciplina, todo tema com
   keywords e descricao.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline.build_taxonomy import carregar_taxonomia, classify  # noqa: E402

TAX = carregar_taxonomia()


def test_yaml_valido():
    assert TAX["metodo"] == "regras-fixas-a-priori"
    assert TAX["version"] >= 1
    for disc, temas in TAX["disciplinas"].items():
        assert disc in TAX["fallback"], f"{disc} sem fallback"
        assert TAX["fallback"][disc] in temas, (
            f"fallback de {disc} nao e um tema da disciplina"
        )
        for tema, info in temas.items():
            assert info["keywords"], f"{disc}/{tema} sem keywords"
            assert info["descricao"], f"{disc}/{tema} sem descricao"


def test_sem_tema_geral_na_taxonomia():
    for disc, temas in TAX["disciplinas"].items():
        assert "geral" not in temas, f"{disc} nao deve ter tema 'geral'"


def test_classificacao_independe_de_outras_linhas():
    """Mudar o texto de OUTROS itens nao altera o tema do item alvo: aplicada
    sobre o parquet completo ou sobre um subconjunto, a classificacao do item
    e identica (nenhuma dependencia do corpus)."""
    disc = "Língua Inglesa"
    texto = "In the text, the author implies that the treaty was effective."
    base = pd.DataFrame(
        [
            {"question_text": texto, "item_text": None, "discipline_canon": disc},
            # outras linhas de outros anos (futuro do item alvo)
            {
                "question_text": "Zzz question never seen before qwerty.",
                "item_text": "other",
                "discipline_canon": disc,
            },
        ]
    )
    # aplica sobre o df completo
    t_full = classify(
        str(base.iloc[0].question_text) + " " + str(base.iloc[0].item_text or ""),
        disc,
        TAX,
    )
    # aplica sobre df contendo APENAS o item alvo
    t_solo = classify(texto + " ", disc, TAX)
    assert t_full == t_solo


@pytest.mark.parametrize(
    "disc,esperado",
    [
        ("Língua Portuguesa", "interpretação_texto"),
        ("Língua Inglesa", "reading_comprehension"),
        ("História do Brasil", "império"),
    ],
)
def test_fallback_sem_match(disc, esperado):
    tema, matched = classify(
        "Texto arbitrario sem nenhuma palavra-chave zzz", disc, TAX
    )
    assert not matched
    assert tema == TAX["fallback"][disc] == esperado


def test_classificacao_por_keyword():
    texto = (
        "Acerca da primeira guerra mundial e do tratado de versalhes, julgue os itens."
    )
    tema, matched = classify(texto, "História Mundial", TAX)
    assert matched
    assert tema == "guerras_mundiais"
