"""Parser CESPE legacy (2003-2018) e discursivas.

Formatos verificados:
  - 1a fase multipla escolha: "QUESTAO N" + comando + alternativas com letra
    em linha propria ("A | texto...") ou "A) texto"
  - 2a/3a fase discursiva: "QUESTAO N" + comando (+ "Valor: X pontos"), sem alternativas
  - secoes de disciplina em CAIXA ALTA
"""

from __future__ import annotations

import re

from parser.document_loader import LoadedDoc
from parser.models import ParsedExam, Question, Alternative, question_id
from parser.parsers.base import (
    DocumentParser,
    is_section_header,
    normalize_disc,
    RE_QUESTION_MARK,
)

RE_ALT_LETTER_ALONE = re.compile(r"^\s*\(?([A-E])\)?\s*$")
RE_ALT_LETTER_INLINE = re.compile(r"^\s*\(?([A-E])\)\s+(.+)$")
RE_VALUE = re.compile(r"(?i)valor[:\s]*([\d,\.]+)\s*(?:pontos|pt)")
ESSAY_HINT = re.compile(
    r"(?i)redija|discorra|elabore|escreva|responda|traduza|vers[eã]o|summar|translation"
)


class CespeLegacyParser(DocumentParser):
    family = "cespe_legacy"

    def matches(self, doc: LoadedDoc) -> bool:
        n = len(RE_QUESTION_MARK.findall(doc.text[:20000]))
        return n >= 2

    def parse(self, doc: LoadedDoc) -> ParsedExam:
        exam = ParsedExam(
            contest_id=doc.contest_id, source_file=doc.source_file, family=self.family
        )
        lines = doc.text.split("\n")
        marks = list(RE_QUESTION_MARK.finditer(doc.text))

        # mapeia offset de cada QUESTAO N para saber o fim do bloco
        line_offsets = []
        pos = 0
        for ln in lines:
            line_offsets.append(pos)
            pos += len(ln) + 1

        def line_of(offset: int) -> int:
            lo, hi = 0, len(line_offsets) - 1
            while lo < hi:
                mid = (lo + hi) // 2
                if line_offsets[mid] < offset:
                    lo = mid + 1
                else:
                    hi = mid
            return lo

        discipline = None
        segments: list[tuple[int, int, str]] = []  # (num, start_line, end_line)
        for idx, m in enumerate(marks):
            start_line = (
                line_of(m.start())
                if m.start() in line_offsets
                else self._line_for_offset(line_offsets, m.start())
            )
            end_line = (
                line_of(marks[idx + 1].start()) - 1
                if idx + 1 < len(marks)
                else len(lines) - 1
            )
            segments.append((int(m.group(1)), start_line, end_line))

        year = doc.year
        phase = (
            2
            if re.search(
                r"(?i)prova escrita|segunda fase|terceira fase|discursiva",
                doc.text[:3000],
            )
            else 1
        )
        stage = (
            "primeira_fase"
            if phase == 1
            else (
                "segunda_fase"
                if "segunda" in doc.text[:3000].lower()
                else "terceira_fase"
            )
        )

        for qnum, s0, s1 in segments:
            block = lines[s0 + 1 : s1 + 1] if s1 > s0 else lines[s0 : s1 + 1]
            # disciplina pode estar no header do bloco (linha antes da QUESTAO em alguns cadernos)
            disc = discipline
            command: list[str] = []
            alternatives: dict[str, list[str]] = {}
            cur_alt: str | None = None
            value = None
            for s in (x.strip() for x in block):
                if not s:
                    continue
                head = is_section_header(s)
                if head:
                    disc = self.normalize_discipline(head)
                    continue
                m_alone = RE_ALT_LETTER_ALONE.match(s)
                m_inline = RE_ALT_LETTER_INLINE.match(s)
                if cur_alt is None and m_alone:
                    cur_alt = m_alone.group(1)
                    alternatives.setdefault(cur_alt, [])
                    continue
                if cur_alt is None and m_inline:
                    cur_alt = m_inline.group(1)
                    alternatives.setdefault(cur_alt, [m_inline.group(2)])
                    continue
                if cur_alt is not None and m_alone:
                    cur_alt = m_alone.group(1)
                    alternatives.setdefault(cur_alt, [])
                    continue
                if cur_alt is not None and m_inline:
                    cur_alt = m_inline.group(1)
                    alternatives.setdefault(cur_alt, [m_inline.group(2)])
                    continue
                vm = None  # (valor de pontos das discursivas tratado futuramente)
                if cur_alt is not None:
                    alternatives[cur_alt].append(s)
                else:
                    command.append(s)

            qtype: str = "multiple_choice" if alternatives else "essay"
            qid = question_id(doc.contest_id, stage, disc, qnum, None)
            cmd_text = " ".join(command).strip()
            rows = []
            if qtype == "multiple_choice":
                rows.append(
                    Question(
                        question_id=qid,
                        contest_id=doc.contest_id,
                        year=year,
                        phase=phase,
                        stage=stage,
                        discipline=disc,
                        question_number=qnum,
                        question_type="multiple_choice",
                        question_text=cmd_text,
                        alternatives=[
                            Alternative(letter=k, text=" ".join(v))
                            for k, v in sorted(alternatives.items())
                        ],
                        source_type=doc.source_type,
                        source_file=doc.source_file,
                    )
                )
            else:
                rows.append(
                    Question(
                        question_id=qid,
                        contest_id=doc.contest_id,
                        year=year,
                        phase=phase,
                        stage=stage,
                        discipline=disc,
                        question_number=qnum,
                        question_type="essay",
                        question_text=cmd_text,
                        source_type=doc.source_type,
                        source_file=doc.source_file,
                        warnings=[]
                        if ESSAY_HINT.search(cmd_text)
                        else ["essay sem verbo de comando"],
                    )
                )
            exam.questions.extend(rows)

        return exam

    @staticmethod
    def _line_for_offset(line_offsets: list[int], offset: int) -> int:
        lo, hi = 0, len(line_offsets) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if line_offsets[mid] <= offset:
                lo = mid + 1
            else:
                hi = mid
        return max(lo - 1, 0)
