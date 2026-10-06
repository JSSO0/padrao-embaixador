"""Parser IADES 2019-2023 (formato certo/errado com questoes compostas).

Verificado no corpus:
  - "QUESTAO N" seguido de grade de numeros de itens (so digitos/espacos)
  - items numerados globalmente (1..N ao longo do caderno), 3-4 por questao
  - layout 2 colunas: o loader (get_text blocks + clusters) ja resolve
"""

from __future__ import annotations

import re

from parser.document_loader import LoadedDoc
from parser.models import ParsedExam, Question, question_id
from parser.parsers.base import (
    DocumentParser,
    is_section_header,
    normalize_disc,
    RE_QUESTION_MARK,
)

RE_ITEM_INLINE = re.compile(r"^\s*(\d{1,3})\s+(.+)$")
RE_GRID_LINE = re.compile(r"^[\s\d\u2500-\u257F|.\-]*$")  # linhas so de numeros/grade
RE_STIMULUS = re.compile(
    r"(?i)(julgue|assinale|de acordo|considere|com base|comando|texto)"
)


class IadesParser(DocumentParser):
    family = "iades"

    def matches(self, doc: LoadedDoc) -> bool:
        if doc.contest_id in ("CACD_2019", "CACD_2020_2021", "CACD_2022", "CACD_2023"):
            return RE_QUESTION_MARK.search(doc.text[:5000]) is not None
        return False

    def parse(self, doc: LoadedDoc) -> ParsedExam:
        exam = ParsedExam(
            contest_id=doc.contest_id, source_file=doc.source_file, family=self.family
        )
        year = int(doc.contest_id.replace("CACD_", "").split("_")[0])
        lines = doc.text.split("\n")

        discipline = None
        expected_item = 1
        q_number = None
        stimulus: list[str] = []
        open_item: int | None = None
        open_lines: list[str] = []
        rows: list[Question] = []
        grid_mode = False  # consumindo grade de numeros no inicio da questao

        def close_item():
            nonlocal open_item, open_lines
            if open_item is None:
                return
            text = " ".join(open_lines).strip()
            if text:
                stage = "primeira_fase"
                rows.append(
                    Question(
                        question_id=question_id(
                            doc.contest_id, stage, discipline, q_number, open_item
                        ),
                        parent_question_id=question_id(
                            doc.contest_id, stage, discipline, q_number, None
                        ),
                        contest_id=doc.contest_id,
                        year=doc.year,
                        phase=1,
                        stage=stage,
                        discipline=discipline,
                        question_number=q_number,
                        item_number=open_item,
                        question_type="certo_errado",
                        question_text=" ".join(stimulus).strip(),
                        item_text=text,
                        source_type=doc.source_type,
                        source_file=doc.source_file,
                    )
                )
            open_item = None
            open_lines = []

        stimulus: list[str] = []
        for ln in lines:
            s = ln.strip()
            if not s:
                continue
            head = is_section_header(s)
            if head:
                close_item()
                discipline = normalize_disc(head)
                stimulus.clear()
                continue
            qm = RE_QUESTION_MARK.match(s)
            if qm:
                close_item()
                q_number = int(qm.group(1))
                stimulus.clear()
                grid_mode = True  # grade de numeros pode vir em seguida
                continue
            # linha-pura-de-numeros = grade (so no comeco da questao)
            if (
                grid_mode
                and re.fullmatch(r"[\s\d|.\-]*", s)
                and any(c.isdigit() for c in s)
                and len(s) < 60
            ):
                continue
            grid_mode = False
            m = RE_ITEM_INLINE.match(s)
            if m:
                num = int(m.group(1))
                # item so inicia se o numero bater com o contador global esperado
                if num == expected_item:
                    close_item()
                    open_item = num
                    open_lines = [m.group(2)]
                    expected_item = num + 1
                    continue
            if open_item is not None:
                # estimulo pode aparecer no meio? raro; assume continuacao do item
                open_lines.append(s)
            else:
                stimulus.append(s)
        close_item()

        exam.questions = rows
        if not rows:
            exam.warnings.append("nenhum item extraido")
        return exam
