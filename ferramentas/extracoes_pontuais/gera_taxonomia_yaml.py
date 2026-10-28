# -*- coding: utf-8 -*-
"""Gera data/metadata/taxonomia.yaml (v1) a partir das regras refinadas de
refine_taxonomy.py + disciplina Cultura Geral. Rodar uma vez."""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pipeline.refine_taxonomy import TAXONOMY  # noqa: E402

DESC = {
    "interpretação_texto": "Compreensão e inferência sobre o conteúdo do texto.",
    "semântica": "Significado, conotação, figuras de linguagem e relações de sentido.",
    "gramática": "Normas gramaticais: concordância, regência, crase, pontuação, ortografia, verbos.",
    "morfossintaxe": "Análise sintática: funções, orações, período composto.",
    "reescrita": "Reescrita de trechos mantendo sentido e correção.",
    "conectivos_e_Referenciação": "Conectivos, referenciação anafórica/catafórica, coesão e coerência.",
    "morfologia": "Classes de palavras e formação (prefixos, sufixos, radicais).",
    "estilo_registro": "Registro formal/informal, norma culta, variação linguística.",
    "tradução": "Tradução e versão de textos.",
    "reading_comprehension": "Compreensão de leitura: inferência e conteúdo do texto.",
    "grammar_semantics": "Gramática e semântica da língua: formas verbais, substituições, estrutura da frase.",
    "vocabulary": "Vocabulário: sinônimos, antônimos e significado de palavras e expressões.",
    "summary_essay": "Resumo, redação e produção escrita.",
    "textual_analysis": "Análise textual: coesão, referência, conectores e estrutura do texto.",
    "colônia": "Brasil colonial: economia açucareira e do ouro, escravidão, administração metropolitana.",
    "império": "Brasil imperial: independência, reinados, monarquia e abolição.",
    "república_velha": "Primeira República: coronelismo, café com leite, oligarquias.",
    "era_vargas": "Era Vargas (1930-1945): Estado Novo, legislação e intervenção estatal.",
    "era_militar": "Regime civil-militar (1964-1985): atos institucionais, repressão e abertura.",
    "nova_república": "Nova República (1985-): redemocratização, Constituição de 1988, crises políticas.",
    "política_externa": "Política externa brasileira por período (pragmatismo responsável, autonomia etc.).",
    "economia_brasileira": "Economia brasileira: industrialização, desenvolvimentismo e planos econômicos.",
    "período_regencial": "Período regencial (1831-1840): revoltas e regências.",
    "revolução_industrial": "Revolução Industrial e consolidação do capitalismo industrial.",
    "revoluções_liberais": "Revoluções liberais, Iluminismo e fim do Antigo Regime.",
    "guerras_mundiais": "Primeira e Segunda Guerras Mundiais: causas, curso e consequências.",
    "guerra_fria": "Guerra Fria: bipolaridade, blocos e confrontos periféricos.",
    "descolonização": "Descolonização afro-asiática, Terceiro Mundo e não-alinhados.",
    "globalização": "Globalização, mundialização e interdependência econômica.",
    "revolução_russa": "Revolução Russa de 1917 e o socialismo soviético.",
    "doutrinas_e_teorias": "Doutrinas de política externa (Monroe, big stick, pan-americanismo) e teorias das RI.",
    "revolução_mexicana": "Revolução Mexicana (1910-1920) e seus protagonistas.",
    "cultura": "Cultura, estética, arte e movimentos intelectuais.",
    "geografia_física": "Meio físico: clima, relevo, vegetação e hidrografia.",
    "geopolítica": "Geopolítica: território, fronteiras, recursos estratégicos e potências.",
    "urbanização": "Urbanização, metropolização e problemas urbanos.",
    "demografia": "População: dinâmicas demográficas e migrações.",
    "agricultura": "Agricultura, estrutura fundiária e mundo rural.",
    "economia_regional": "Desenvolvimento e desigualdades regionais.",
    "meio_ambiente": "Questão ambiental, clima e sustentabilidade.",
    "multilateralismo": "Organizações e regimes multilaterais (ONU, OMC, FMI, Banco Mundial).",
    "teorias_RI": "Teorias das Relações Internacionais.",
    "integração_regional": "Integração regional: Mercosul, União Europeia, blocos econômicos.",
    "política_externa_brasileira": "Política externa brasileira e inserção internacional do país.",
    "segurança_internacional": "Segurança internacional: conflitos, armas e desarmamento.",
    "direitos_humanos": "Direitos humanos, refugiados e agenda humanitária.",
    "meio_ambiente": "Meio ambiente e clima nas relações internacionais.",
    "doutrinas": "Doutrinas de política externa (Monroe, big stick, pan-americanismo).",
    "microeconomia": "Microeconomia: oferta, demanda, estruturas de mercado e elasticidade.",
    "macroeconomia": "Macroeconomia: agregados, inflação, política monetária e fiscal.",
    "comércio_internacional": "Comércio internacional, teoria do comércio e balanço de pagamentos.",
    "desenvolvimento": "Desenvolvimento econômico, pobreza e desigualdade.",
    "monetário": "Moeda, sistema financeiro e política monetária.",
    "finanças_públicas": "Finanças públicas: tributação, orçamento e dívida.",
    "economia_internacional": "Economia internacional: globalização e fluxos de capitais.",
    "constitucional": "Direito constitucional: CF de 1988, controle de constitucionalidade e STF.",
    "internacional_público": "Direito internacional público: tratados, sujeitos e tribunais internacionais.",
    "organização_do_estado": "Organização do Estado brasileiro e poderes.",
    "direito_administrativo": "Direito administrativo: administração pública e atos administrativos.",
    "mercosul_direito": "Direito do Mercosul.",
    "cultura": "Cultura e sociedade: aspectos estéticos e múltiplos aspectos culturais.",
}

FALLBACK = {
    "Língua Portuguesa": "interpretação_texto",
    "Língua Inglesa": "reading_comprehension",
    "História do Brasil": "império",
    "História Mundial": "guerras_mundiais",
    "Geografia": "geopolítica",
    "Política Internacional": "multilateralismo",
    "Economia": "microeconomia",
    "Direito": "constitucional",
}

disciplinas = {}
for disc, temas in TAXONOMY.items():
    disc_out = {}
    for tema, kws in temas:
        disc_out[tema] = {
            "descricao": DESC.get(tema, ""),
            "keywords": kws,
        }
    disciplinas[disc] = dict(sorted(disc_out.items()))

FB = {
    "Língua Portuguesa": "interpretação_texto",
    "Língua Inglesa": "reading_comprehension",
    "História do Brasil": "império",
    "História Mundial": "guerras_mundiais",
    "Geografia": "geopolítica",
    "Política Internacional": "multilateralismo",
    "Economia": "microeconomia",
    "Direito": "constitucional",
}
# disciplina extra (2004 q141-150)
disciplinas["Cultura Geral"] = {
    "cultura": {
        "descricao": DESC["cultura"],
        "keywords": ["cultura", "cultural", "estética", "arte", "cinema", "literatura"],
    }
}
FB["Cultura Geral"] = "cultura"

doc = {
    "taxonomia": {
        "version": 1,
        "data_versao": "2026-10-28",
        "metodo": "regras-fixas-a-priori",
        "descricao": (
            "Temas por disciplina da 1a fase. Atribuicao por contagem de "
            "palavras-chave no enunciado+item; sem match, aplica-se o fallback "
            "da disciplina (tema mais amplo). Nenhuma etapa usa o corpus "
            "completo: a classificacao de um item depende apenas do seu texto "
            "e deste arquivo (sem vazamento temporal)."
        ),
        "fallback": FB,
        "disciplinas": disciplinas,
    }
}

out = Path(__file__).resolve().parents[2] / "data/metadata/taxonomia.yaml"
out.write_text(
    yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100),
    encoding="utf-8",
)
print(f"ok: {out}")
