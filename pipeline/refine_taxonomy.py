"""Taxonomia refinada: mais keywords para reduzir o tema 'geral' e cobrir os
subtemas identificados na análise dos enunciados. Aplica no parquet."""

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/processed/questions.parquet"
df = pd.read_parquet(PATH)

TAXONOMY = {
    "Língua Portuguesa": [
        (
            "interpretação_texto",
            [
                "interpretação",
                "sentido do texto",
                "ideias do texto",
                "compreensão",
                "infer",
                "deduz",
                "permite supor",
                "permite inferir",
                "depreende-se",
                "infere-se",
                "pode-se inferir",
            ],
        ),
        (
            "semântica",
            [
                "semântica",
                "sentido",
                "significado",
                "conotação",
                "denotação",
                "figura de linguagem",
                "metáfora",
                "metonímia",
                "ironia",
                "hipérbole",
                "antítese",
                "polissemia",
                "sinonimia",
                "antonimia",
                "ambiguidade",
                "denotativo",
                "conotativo",
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
                "verbos",
                "tempos verbais",
                "modos verbais",
                "vozes verbais",
                "voz passiva",
                "voz ativa",
                "voz reflexiva",
                "sintático",
                "morfológico",
                "gramatical",
            ],
        ),
        (
            "morfossintaxe",
            [
                "morfossintático",
                "morfossintático",
                "função sintática",
                "sujeito",
                "objeto direto",
                "objeto indireto",
                "predicado",
                "adjunto",
                "aposto",
                "vocativo",
                "oração subordinada",
                "oração coordenada",
                "período composto",
                "período simples",
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
                "sem alterar o sentido",
                "sem alterar",
                "substituído por",
                "substituição de",
            ],
        ),
        (
            "conectivos_e_Referenciação",
            [
                "conector",
                "conectivo",
                "referência",
                "anafórico",
                "catáforo",
                "elipse",
                "coerência",
                "coesão",
                "articulação",
                "conector",
                "conjunção",
            ],
        ),
        (
            "morfologia",
            [
                "morfologia",
                "classe de palavras",
                "substantivo",
                "adjetivo",
                "advérbio",
                "pronome",
                "preposição",
                "conjunção",
                "artigo",
                "prefixo",
                "sufixo",
                "radical",
                "desinência",
                "aumento",
                "diminutivo",
            ],
        ),
        (
            "estilo_registro",
            [
                "linguagem formal",
                "linguagem informal",
                "registro",
                "registro culto",
                "coloquial",
                "variação linguística",
                "linguagem conotativa",
                "linguagem denotativa",
                "norma culta",
                "norma padrão",
            ],
        ),
        ("tradução", ["tradução", "versão", "transposição", "traduzir"]),
    ],
    "Língua Inglesa": [
        (
            "reading_comprehension",
            [
                "inferred",
                "according to",
                "the author",
                "in the text",
                "based on the text",
                "reading",
                "comprehension",
                "text refers",
                "text suggests",
                "imply",
                "meaning",
            ],
        ),
        (
            "grammar_semantics",
            [
                "grammatical",
                "semantic",
                "verb form",
                "word",
                "replaced",
                "substituted",
                "meaning of",
                "fragment",
                "sentence",
                "function of",
            ],
        ),
        (
            "vocabulary",
            [
                "vocabulary",
                "word",
                "expression",
                "meaning",
                "synonym",
                "antonym",
                "noun",
                "verb",
                "adjective",
            ],
        ),
        ("translation", ["translation", "translate", "versão", "tradução"]),
        (
            "summary_essay",
            ["summary", "essay", "write", "discuss", "resumo", "redação"],
        ),
        (
            "textual_analysis",
            [
                "paragraph",
                "textual",
                "cohesion",
                "coherence",
                "reference",
                "pronoun",
                "connector",
                "discourse marker",
                "text structure",
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
                "palmares",
                "quilombo",
                "portugal",
                "metrópole",
                "engenho",
                "companhia",
                "jesuítas",
                "bandeirantes",
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
                "primeiro reinado",
                "segundo reinado",
                "leí áurea",
                "eliana",
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
                "proclamação da república",
                "canudos",
                "contestado",
            ],
        ),
        (
            "era_vargas",
            [
                "vargas",
                "estado novo",
                "getúlio",
                "1930",
                "1945",
                "constituição de 1934",
                "intervencionista",
            ],
        ),
        (
            "era_militar",
            [
                "regime militar",
                "1964",
                "ditadura",
                "AI-5",
                "anistia",
                "abertura",
                "golpe militar",
                "atos institucionais",
            ],
        ),
        (
            "nova_república",
            [
                "nova república",
                "1985",
                "collor",
                "impeachment",
                "diretas já",
                "constituição de 1988",
                "plano cruzado",
                "partido comunista",
                "jânio quadros",
                "UDN",
            ],
        ),
        (
            "política_externa",
            [
                "política externa",
                "relações exteriores",
                "política externa brasileira",
                "inserção internacional",
                "cancún",
                "brasil-argentina",
                "brasil-argentina",
                "pragmatismo responsável",
                "autonomia",
                "riozinho",
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
                "guerra fiscal",
                "Estado desenvolvimentista",
            ],
        ),
        (
            "período_regencial",
            [
                "período regencial",
                "regência",
                "cabanagem",
                "farroupilha",
                "balaiada",
                "sabinada",
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
                "arkwright",
                "bastidor",
                "maquinofatura",
                "manufatura",
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
                "napoleão",
                "burguesia",
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
                "tratado de versalhes",
                "liga das nações",
            ],
        ),
        (
            "guerra_fria",
            [
                "guerra fria",
                "URSS",
                "bipolaridade",
                "containment",
                "Cortina de Ferro",
                "otan",
                "pacto de varsóvia",
                "guerra do vietnã",
                "crise dos mísseis",
            ],
        ),
        (
            "descolonização",
            [
                "descolonização",
                "terceiro mundo",
                "não-alinhados",
                "colonialismo",
                "Ásia",
                "áfrica colonial",
                "china",
                "império colonial",
                "imperialismo",
            ],
        ),
        (
            "globalização",
            [
                "globalização",
                "mundialização",
                "internet",
                "multinacional",
                "interdependência",
                "global",
            ],
        ),
        (
            "revolução_russa",
            [
                "revolução russa",
                "lenin",
                "bolchevique",
                "stalin",
                "união soviética",
                "1917",
            ],
        ),
        (
            "doutrinas_e_teorias",
            [
                "doutrina monroe",
                "destino manifesto",
                "pan-americanismo",
                "big stick",
                "escola de copenhague",
                "realismo",
                "liberalismo",
            ],
        ),
        (
            "revolução_mexicana",
            ["revolução mexicana", "obregón", "villa", "zapata", "mexicano"],
        ),
        (
            "cultura",
            [
                "padrões culturais",
                "estéticos",
                "modernismo",
                "vanguarda",
                "arte",
                "cinema",
                "literatura",
            ],
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
                "biomas",
                "águas",
                "floresta",
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
                "poder mundial",
                "oriente médio",
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
                "metrópole",
                "crescimento urbano",
            ],
        ),
        (
            "demografia",
            [
                "demografia",
                "população",
                "migração",
                "migratório",
                "densidade",
                "natalidade",
                "mortalidade",
                "transição demográfica",
                "crescimento populacional",
                "envelhecimento",
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
                "modernização da agricultura",
            ],
        ),
        (
            "economia_regional",
            [
                "desenvolvimento regional",
                "política fiscal",
                "guerra fiscal",
                "industrialização brasileira",
                "divisão regional",
                "região nordeste",
            ],
        ),
        (
            "meio_ambiente",
            [
                "meio ambiente",
                "ambiental",
                "clima",
                "biodiversidade",
                "sustentável",
                "desmatamento",
            ],
        ),
    ],
    "Política Internacional": [
        (
            "multilateralismo",
            [
                "ONU",
                "nações unidas",
                "conselho de segurança",
                "assembleia geral",
                "multilateral",
                "organismo internacional",
                "corte internacional",
                "fórum",
                "tribunal internacional",
                "OMC",
                "FMI",
                "banco mundial",
            ],
        ),
        (
            "teorias_RI",
            [
                "escola de copenhague",
                "realismo",
                "liberalismo",
                "teoria das relações",
                "escola teórica",
                "perspectivas teóricas",
                "construtivismo",
                "securitização",
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
                "bloco econômico",
                "tratado de assunção",
                "BASIC",
                "IBSA",
                "BRICS",
            ],
        ),
        (
            "política_externa_brasileira",
            [
                "política externa brasileira",
                "inserção internacional do brasil",
                "diplomacia brasileira",
                "brasil no mundo",
                "política externa adotada",
                "relações do brasil",
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
                "URSS",
            ],
        ),
        (
            "segurança_internacional",
            [
                "segurança",
                "conflito",
                "guerra",
                "armas",
                "desarmamento",
                "nuclear",
                "armamentos estratégicos",
                "uso da força",
            ],
        ),
        (
            "direitos_humanos",
            [
                "direitos humanos",
                "apátridas",
                "refugiados",
                "migrantes",
                "humanitário",
                "intervenção humanitária",
            ],
        ),
        (
            "meio_ambiente",
            [
                "meio ambiente",
                "clima",
                "desenvolvimento sustentável",
                "ambiental",
                "mudança climática",
                "questão ambiental",
            ],
        ),
        (
            "doutrinas",
            [
                "doutrina monroe",
                "destino manifesto",
                "big stick",
                "pan-americanismo",
                "escola de copenhague",
            ],
        ),
    ],
    "Economia": [
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
                "microeconômica",
                "curva de demanda",
                "curva de oferta",
                "equilíbrio",
            ],
        ),
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
                "produto interno bruto",
                "crescimento econômico",
                "desemprego",
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
                "vantagem comparativa",
                "hecksher-ohlin",
                "economia internacional",
                "mercado internacional",
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
                "subdesenvolvimento",
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
                "M1",
                "oferta de moeda",
                "demanda de moeda",
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
                "desemprego",
                "salário mínimo",
            ],
        ),
        (
            "economia_internacional",
            [
                "economia internacional",
                "globalização econômica",
                "fluxo de capitais",
                "globalização do espaço",
            ],
        ),
    ],
    "Direito": [
        (
            "constitucional",
            [
                "constituição",
                "CF",
                "constitucionalidade",
                "STF",
                "direitos fundamentais",
                "controle de constitucionalidade",
                "constitucional",
                "supremo tribunal federal",
                "poderes",
                "processo legislativo",
            ],
        ),
        (
            "internacional_público",
            [
                "tratado internacional",
                "Corte Internacional de Justiça",
                "direito internacional público",
                "Estado estrangeiro",
                "soberania",
                "extradição",
                "jus cogens",
                "preâmbulo dos tratados",
                "tribunais internacionais",
                "direito internacional do meio ambiente",
                "direitos humanos",
                "humanitário",
                "privilégios e imunidades",
                "acreditantes",
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
                "conselho da república",
                "organização dos poderes",
            ],
        ),
        (
            "direito_administrativo",
            [
                "administração pública",
                "servidor público",
                "ato administrativo",
                "licitação",
                "direito administrativo brasileiro",
            ],
        ),
        (
            "mercosul_direito",
            [
                "mercosul",
                "tratado de assunção",
                "declaração do iguaçu",
                "brasil-argentina",
            ],
        ),
    ],
}


def classify(text: str, discipline: str) -> str:
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
    print("=== Taxonomia refinada aplicada ===")
    geral_total = 0
    total = 0
    for disc in sorted(TAXONOMY):
        sub = df[df.stage.eq("primeira_fase") & df.discipline_canon.eq(disc)]
        c = sub["topic"].value_counts().to_dict()
        geral = c.pop("geral", 0)
        geral_total += geral
        print(f"  {disc}: {c} | geral: {geral}")
    print(f"  TOTAL geral: {geral_total} de {len(sub)}")


if __name__ == "__main__":
    main()
