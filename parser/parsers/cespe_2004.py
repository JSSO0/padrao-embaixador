"""Parser CESPE 2004-2006 (julgue-o-item com marcador "N ?" tipo bullet).

Decodificado por inspecao (docs/inspecao-formatos.md + blocos com x/y):
  - itens marcados como "1 ? A expressao ..." (numero + simbolo CESPE que
    aparece como "?" no texto extraido)
  - 150 itens globais (1..150), texto-base por bloco "Texto I - itens de 1 a 15"
  - disciplina em CAIXA ALTA centralizada (PORTUGUES, CULTURA GERAL...)
  - pagina 2 coluna unica; demais 2 colunas (loader resolve via gutter)
"""

from __future__ import annotations

import re

from parser.document_loader import LoadedDoc
from parser.models import ParsedExam, Question, question_id
from parser.parsers.base import DocumentParser, normalize_disc

RE_ITEM_MARK = re.compile(r"^\s*(\d{1,3})\s*[:\?\.\)\u2022\u25cf\u00b7]\s*(\S.*)$")
RE_TEXTO_RANGE = re.compile(
    r"(?i)Texto\s+\S+\s*[-–—]\s*itens?\s+de\s+(\d+)\s+a\s+(\d+)"
)
RE_DISCIPLINE = re.compile(r"^[A-ZÀ-Ü][A-ZÀ-Ü\s]{4,30}$")
RE_COMMAND = re.compile(r"(?i)julgue os itens")
RE_FOOTER = re.compile(r"(?i)UnB\s*/\s*CESPE|Cargo: Terceiro")


class CespeJulgueParser(DocumentParser):
    family = "cespe_julgue"

    def matches(self, doc: LoadedDoc) -> bool:
        n = sum(1 for ln in doc.text.split("\n") if RE_ITEM_MARK.match(ln))
        return n >= 10

    def parse(self, doc: LoadedDoc) -> ParsedExam:
        exam = ParsedExam(
            contest_id=doc.contest_id, source_file=doc.source_file, family=self.family
        )
        lines = doc.text.split("\n")

        discipline = None
        expected_item = 1
        command: list[str] = []
        rows: list[Question] = []
        open_item: int | None = None
        open_lines: list[str] = []

        def close_item() -> None:
            nonlocal open_item, open_lines
            if open_item is None:
                return
            text = " ".join(open_lines).strip()
            if text:
                rows.append(
                    Question(
                        question_id=question_id(
                            doc.contest_id, "primeira_fase", discipline, open_item, None
                        ),
                        contest_id=doc.contest_id,
                        year=doc.year,
                        phase=1,
                        stage="primeira_fase",
                        discipline=discipline,
                        question_number=open_item,
                        question_type="certo_errado",
                        question_text=" ".join(command).strip(),
                        item_text=text,
                        source_type=doc.source_type,
                        source_file=doc.source_file,
                    )
                )
            open_item = None
            open_lines = []

        for s in (ln.strip() for ln in lines):
            if not s:
                continue
            if RE_FOOTER.search(s) and len(s) < 120:
                continue
            if RE_DISCIPLINE.match(s) and "itens" not in s.lower():
                close_item()
                discipline = normalize_disc(s)
                continue
            mrange = re.match(
                r"(?i)Texto\s+\S+\s*[-–—]\s*itens?\s+de\s+(\d+)\s+a\s+(\d+)", s
            )
            if mrange:
                close_item()
                expected_item = int(mrange.group(1))
                command.clear()
                continue
            m = RE_ITEM_MARK.match(s)
            if m:
                close_item()
                open_item = int(m.group(1))
                open_lines = [m.group(2)]
                continue
            if RE_COMMAND.search(s):
                command.clear()
                command.append(s)
                continue
            if open_item is not None:
                open_lines.append(s)
            else:
                command.append(s)
        close_item()

        exam.questions = rows
        if not rows:
            exam.warnings.append("nenhum item extraido")
        return exam
