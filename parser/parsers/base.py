"""Base dos parsers de questoes + factory.

Regra de ouro: parser novo = arquivo novo + fixtures de teste. Regex ficam
dentro da classe do parser; thresholds em configs/segmentation.yaml.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod

from parser.document_loader import LoadedDoc
from parser.models import ParsedExam

SECTION_STOPWORDS = {
    "PROVA OBJETIVA",
    "PROVA DISCURSIVA",
    "PROVA ESCRITA",
    "CADERNO DE PROVAS",
    "ESPACO LIVRE",
    "ESPAÇO LIVRE",
    "CEBRASPE",
    "IADES",
    "CONHECIMENTOS BÁSICOS",
    "CONHECIMENTOS GERAIS",
    "CONHECIMENTOS ESPECÍFICOS",
    "FOLHA DE RESPOSTAS",
    "FOLHA DE RASCUNHO",
}

DISCIPLINE_NORMALIZE = {
    "LÍNGUA PORTUGUESA": "Língua Portuguesa",
    "LÍNGUA INGLESA": "Língua Inglesa",
    "LÍNGUA ESPANHOLA E LÍNGUA FRANCESA": "Espanhol e Francês",
    "HISTÓRIA DO BRASIL": "História do Brasil",
    "HISTÓRIA MUNDIAL": "História Mundial",
    "HISTÓRIA GERAL": "História Mundial",
    "GEOGRAFIA": "Geografia",
    "POLÍTICA INTERNACIONAL": "Política Internacional",
    "ECONOMIA": "Economia",
    "NOÇÕES DE ECONOMIA": "Economia",
    "DIREITO": "Direito",
    "NOÇÕES DE DIREITO E DIREITO INTERNACIONAL PÚBLICO": "Direito",
    "DIREITO INTERNACIONAL": "Direito",
    "TEORIA DAS RELAÇÕES INTERNACIONAIS": "Política Internacional",
    "HISTÓRIA DAS RELAÇÕES INTERNACIONAIS": "História Mundial",
    "GEOPOLÍTICA": "Geografia",
    "ESPAÑOL Y FRANCÉS": "Espanhol e Francês",
}

RE_QUESTION_MARK = re.compile(r"QUEST[ÃA]O\s+(\d{1,3})")


def is_section_header(line: str) -> str | None:
    s = " ".join(line.split())
    if len(s) < 4 or len(s) > 60 or "--" in s:
        return None
    if any(c.isdigit() for c in s):
        return None
    if s != s.upper():
        return None
    if any(
        w in s for w in ("CEBRASPE", "IADES", "EDITAL", "CADERNO", "FOLHA", "CONCURSO")
    ):
        return None
    if "PROVA" in s or "LIVRE" in s:
        return None
    return s


def normalize_disc(raw: str) -> str:
    s = " ".join(raw.split()).upper().rstrip(". ")
    if s in DISCIPLINE_NORMALIZE:
        return DISCIPLINE_NORMALIZE[s]
    return s.title()


class DocumentParser(ABC):
    family: str = ""

    @abstractmethod
    def matches(self, doc: LoadedDoc) -> bool:
        """Decide se este parser atende o documento."""

    @abstractmethod
    def parse(self, doc: LoadedDoc) -> ParsedExam:
        """Extrai questoes de um documento carregado."""


def get_parser(doc: LoadedDoc) -> DocumentParser:
    """Escolhe parser por familia/ano/padroes. Fallback: cespe_legacy."""
    from parser.parsers.cebraspe_modern import CebraspeModernParser
    from parser.parsers.iades import IadesParser
    from parser.parsers.cespe_legacy import CespeLegacyParser

    for p in (CebraspeModernParser(), IadesParser(), CespeLegacyParser()):
        if p.matches(doc):
            return p
    return CespeLegacyParser()
