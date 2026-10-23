"""Taxonomia temática inicial: classifica os 4.951 itens da 1a fase por
tema dentro de cada disciplina usando palavras-chave no enunciado e texto.

Salva no parquet como coluna `topic`.
"""

import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PATH = "data/processed/questions.parquet"
df = pd.read_parquet(PATH)

# Taxonomia inicial: temas por disciplina, definidos a partir da análise
# dos enunciados reais. Cada tema tem keywords que aparecem no enunciado.
TAXONOMY = {
    "Língua Portuguesa": [
        (
            "interpretação",
            [
                "interpretação",
                "sentido do texto",
                "ideias do texto",
                "compreensão",
                "infer",
                "deduz",
            ],
        ),
        (
            "gramática",
            [
                "concordância",
                "regência",
                "crase",
                "pontuação",
                "ortografia",
                "emprego de",
                "colocação",
                "oração",
                "sintaxe",
                "fonética",
                "morfologia",
                "sintaxe",
                "verbos",
                "tempos verbais",
            ],
        ),
        (
            "reescrita",
            [
                "reescrita",
                "reescreva",
                "mantendo",
                "equivalência de sentido",
                "substituição",
                "reescritura",
            ],
        ),
        (
            "semântica",
            [
                "significado",
                "sentido",
                "semântica",
                "conotação",
                "denotação",
                "figuras de linguagem",
                "metáfora",
                "metonímia",
                "ironia",
            ],
        ),
        (
            "morfologia",
            [
                "morfológico",
                "classe de palavras",
                "substantivo",
                "adjetivo",
                "advérbio",
                "pronome",
                "preposição",
                "conjunção",
                "artigo",
                "sujeito",
                "objeto",
            ],
        ),
        (
            "funções da linguagem",
            [
                "função referencial",
                "função metalinguística",
                "função emotiva",
                "função fática",
                "função poética",
                "função conativa",
            ],
        ),
        (
            "estilo",
            [
                "linguagem formal",
                "linguagem informal",
                "registro",
                "registro culto",
                "linguagem coloquial",
                "variação linguística",
            ],
        ),
    ],
    "Língua Inglesa": [
        (
            "reading_comprehension",
            [
                "it can be inferred",
                "according to the text",
                "the author",
                "in the text",
                "compreensão de texto",
                "reading comprehension",
                "based on the text",
                "according to",
            ],
        ),
        ("translation", ["tradução", "translation", "translate", "versão"]),
        ("summary", ["summary", "resumo", "summarize"]),
        ("essay", ["essay", "redação", "write", "discuss"]),
        (
            "grammar",
            [
                "grammar",
                "passive voice",
                "reported speech",
                "conditionals",
                "verb tenses",
                "phrasal",
            ],
        ),
    ],
    "História do Brasil": [
        (
            "colônia",
            [
                "colonização",
                "colônia",
                "ciclos econômicos",
                "açúcar",
                "ouro",
                "escravidão",
                "capitania",
                "companhia de comércio",
                "palmares",
                "quilombo",
            ],
        ),
        (
            "império",
            [
                "império",
                "independência",
                "dom Pedro",
                "regência",
                "monarquia",
                "abolição",
                "1850",
                "1822",
                "1891",
                "reino unido",
            ],
        ),
        (
            "república_velha",
            [
                "república velha",
                "coronelismo",
                "1889",
                "primeira república",
                "café",
                "oligarquia",
            ],
        ),
        ("era_vargas", ["vargas", "estado novo", "getúlio", "1930", "1945"]),
        (
            "era_militar",
            ["regime militar", "1964", "ditadura", "AI-5", "anistia", "abertura"],
        ),
        (
            "nova_república",
            ["nova república", "1985", "collor", "impeachment", "fome zero"],
        ),
        (
            "política_externa",
            [
                "política externa",
                "relações exteriores",
                "política externa brasileira",
                "inserção internacional",
            ],
        ),
        (
            "economia_brasileira",
            [
                "ciclos econômicos",
                "industrialização",
                "desenvolvimentismo",
                "plano cruzado",
                "inflação brasileira",
                "importação substituição",
            ],
        ),
    ],
    "História Mundial": [
        (
            "revolução_industrial",
            [
                "revolução industrial",
                "industrialização",
                "capitalismo",
                "inglaterra",
                "século XIX",
                "revolução tecnológica",
            ],
        ),
        (
            "revoluções_liberais",
            [
                "revolução francesa",
                "revolução americana",
                "liberalismo",
                "iluminismo",
                "ilustração",
                "antigo regime",
            ],
        ),
        (
            "guerras_mundiais",
            [
                "primeira guerra",
                "segunda guerra",
                "guerra mundial",
                "nazismo",
                "fascismo",
                "holocausto",
                "1914",
                "1939",
                "1945",
            ],
        ),
        (
            "guerra_fria",
            [
                "guerra fria",
                "URSS",
                "capitalismo socialista",
                "bipolaridade",
                "containment",
                "Cortina de Ferro",
            ],
        ),
        (
            "descolonização",
            [
                "descolonização",
                "terceiro mundo",
                "não-alinhados",
                "Naçãos Unidas",
                "colonialismo",
            ],
        ),
        (
            "globalização",
            ["globalização", "mundialização", "internet", "multinacional"],
        ),
        (
            "revolução_russa",
            ["revolução russa", "lenin", "bolchevique", "stalin", "união soviética"],
        ),
    ],
    "Geografia": [
        (
            "geografia_física",
            [
                "clima",
                "relevo",
                "vegetação",
                "hidrografia",
                "meio ambiente",
                "ambiental",
                "biodiversidade",
                "recursos hídricos",
            ],
        ),
        (
            "geopolítica",
            [
                "geopolítica",
                "território",
                "fronteira",
                "recursos estratégicos",
                "ordem mundial",
                "cenário geopolítico",
            ],
        ),
        (
            "urbanização",
            [
                "urbanização",
                "cidades",
                "favela",
                "conurbação",
                "metropolização",
                "êxodo rural",
                "população urbana",
            ],
        ),
        (
            "agricultura",
            [
                "agricultura",
                "agrícola",
                "rural",
                "agronegócio",
                "reforma agrária",
                "campesinato",
            ],
        ),
        ("globalização", ["globalização", "mundialização", "multinacional", "global"]),
        (
            "economia_regional",
            [
                "desenvolvimento regional",
                "política fiscal",
                "guerra fiscal",
                "industrialização brasileira",
            ],
        ),
    ],
    "Política Internacional": [
        (
            "ONU_multilateral",
            [
                "ONU",
                "nações unidas",
                "conselho de segurança",
                "assembleia geral",
                "multilateral",
                "organismo internacional",
                "corte internacional",
            ],
        ),
        (
            "guerra_fria",
            [
                "guerra fria",
                "bipolaridade",
                "otan",
                "pacto de varsóvia",
                "conflito leste-oeste",
            ],
        ),
        (
            "integração_regional",
            [
                "mercosul",
                "integração regional",
                "união europeia",
                "integração econômica",
                "regionalização",
            ],
        ),
        (
            "política_externa_brasileira",
            [
                "política externa brasileira",
                "inserção internacional do brasil",
                "diplomacia brasileira",
                "brasil no mundo",
            ],
        ),
        ("globalização", ["globalização", "mundialização", "interdependência"]),
        (
            "segurança",
            ["segurança", "conflito", "guerra", "armas", "desarmamento", "nuclear"],
        ),
        (
            "ambiental",
            ["meio ambiente", "clima", "desenvolvimento sustentável", "ambiental"],
        ),
    ],
    "Economia": [
        (
            "macroeconomia",
            [
                "PIB",
                "inflação",
                "juros",
                "política monetária",
                "política fiscal",
                "demanda agregada",
                "monetária",
            ],
        ),
        (
            "microeconomia",
            [
                "demanda",
                "oferta",
                "elasticidade",
                "monopólio",
                "oligopólio",
                "concorrência",
                "mercado",
            ],
        ),
        (
            "comércio_internacional",
            [
                "comércio internacional",
                "exportação",
                "importação",
                "balanço de pagamentos",
                "câmbio",
                "tarifa",
            ],
        ),
        (
            "desenvolvimento",
            [
                "desenvolvimento econômico",
                "crescimento",
                "pobreza",
                "desigualdade",
                "distribuição de renda",
            ],
        ),
        (
            "finanças_públicas",
            [
                "imposto",
                "tributo",
                "orçamento",
                "déficit público",
                "dívida pública",
                "tributação",
            ],
        ),
        (
            "monetário",
            [
                "moeda",
                "banco central",
                "meios de pagamento",
                "política monetária",
                "inflação",
            ],
        ),
    ],
    "Direito": [
        (
            "direito_constitucional",
            [
                "constituição",
                "CF",
                "constitucionalidade",
                "STF",
                "direitos fundamentais",
                "controle de constitucionalidade",
            ],
        ),
        (
            "direito_internacional",
            [
                "tratado internacional",
                "Corte Internacional de Justiça",
                "direito internacional público",
                "Estado estrangeiro",
                "soberania",
                "extradição",
            ],
        ),
        (
            "organização_do_estado",
            [
                "organização do estado",
                "poderes",
                "presidente",
                "congresso",
                "supremo",
                "federal",
                "tribunal",
            ],
        ),
        (
            "direito_administrativo",
            [
                "administração pública",
                "servidor público",
                "ato administrativo",
                "licitação",
            ],
        ),
    ],
}


def classify(text: str, discipline: str) -> str:
    """Classifica o item pelo tema, usando as palavras-chave da taxonomia."""
    themes = TAXONOMY.get(discipline, [])
    if not themes:
        return "geral"
    lower = text.lower()
    best_theme, best_score = "geral", 0
    for theme, kws in themes:
        score = sum(1 for kw in kws if kw.lower() in lower)
        if score > best_score:
            best_theme, best_score = theme, score
    return best_theme


def main() -> None:
    df = pd.read_parquet(PATH)
    m = (
        df.stage.eq("primeira_fase")
        & df.discipline_canon.notna()
        & df.discipline_canon.isin(TAXONOMY)
    )
    df["topic"] = None
    for idx in df.index[m]:
        text = (
            str(df.at[idx, "question_text"]) + " " + str(df.at[idx, "item_text"] or "")
        )
        disc = df.at[idx, "discipline_canon"]
        df.at[idx, "topic"] = classify(text, disc)
    df.to_parquet(PATH, index=False)
    print("=== Taxonomia aplicada ===")
    for disc in sorted(TAXONOMY):
        sub = df[df.stage.eq("primeira_fase") & df.discipline_canon.eq(disc)]
        c = sub["topic"].value_counts().to_dict()
        print(f"  {disc}: {c}")


if __name__ == "__main__":
    main()
