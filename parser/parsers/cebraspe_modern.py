"""Parser para o formato Cebraspe 2024-2026 (verificado no corpus real).

Formato:
  - secoes de disciplina em CAIXA ALTA (LINGUA PORTUGUESA, HISTORIA DO BRASIL...)
  - itens certo/errado com numero inline no inicio da linha ("151 Autores
    associados...") ou numero solto na linha; numeracao continua entre cadernos
  - comandos ("julgue os itens seguintes") e estímulos aparecem entre itens
Regras puras, sem IA. QA: docs/spec-etapa5.md
"""

from __future__ import annotations

import re

from parser.document_loader import LoadedDoc
from parser.models import ParsedExam, Question, question_id
from parser.parsers.base import DocumentParser, is_section_header, normalize_disc

RE_ITEM_INLINE = re.compile(r"^\s*(\d{1,3})\s+(\S.*)$")
RE_ITEM_ALONE = re.compile(r"^\s*(\d{1,3})\s*$")
START_TRIGGER = re.compile(r"-- PROVA OBJETIVA --|PROVA OBJETIVA", re.IGNORECASE)
HEADER_NOISE = re.compile(r"(?i)cebraspe|edital|folha de respostas|caderno de prova")


class CebraspeModernParser(DocumentParser):
    family = "cebraspe_modern"

    def matches(self, doc: LoadedDoc) -> bool:
        if doc.family != "cebraspe" and doc.family != "cursocacd":
            return False
        if doc.contest_id < "CACD_2024":
            return False
        # precisa ter itens inline OU numero solto em sequencia
        nums = self._candidate_numbers(doc)
        return len(nums) >= 10

    @staticmethod
    def _candidate_numbers(doc: LoadedDoc) -> list[int]:
        out = []
        for ln in doc.text.split("\n"):
            m = RE_ITEM_INLINE.match(ln) or RE_ITEM_ALONE.match(ln)
            if m:
                out.append(int(m.group(1)))
        return out

    def parse(self, doc: LoadedDoc) -> ParsedExam:
        exam = ParsedExam(
            contest_id=doc.contest_id, source_file=doc.source_file, family=self.family
        )
        year = int(doc.contest_id.replace("CACD_", "").split("_")[0])
        lines = (doc.linear_text or doc.text).split("\n")

        # comeca apos o gatilho de prova (ou do inicio se nao achar)
        start = 0
        for i, ln in enumerate(lines):
            if START_TRIGGER.search(ln):
                start = i + 1
                break

        discipline: str | None = None
        # semeia o contador pelo primeiro candidato que inicia uma sequencia n, n+1
        cand = self._candidate_numbers(doc)
        expected_next = 1
        for j in range(len(cand) - 1):
            if cand[j + 1] == cand[j] + 1:
                expected_next = cand[j]
                break
        context: list[str] = []  # paragrafos entre itens (comando/estimulo)
        open_item: int | None = None
        open_item_lines: list[str] = []
        rows: list[Question] = []

        def close_item():
            nonlocal open_item, open_item_lines
            if open_item is None:
                return
            text = " ".join(open_item_lines).strip()
            if text and open_item is not None:
                qid = question_id(
                    doc.contest_id, "primeira_fase", discipline, None, open_item
                )
                rows.append(
                    Question(
                        question_id=qid,
                        contest_id=doc.contest_id,
                        year=year,
                        phase=1,
                        stage="primeira_fase",
                        discipline=discipline,
                        question_number=None,
                        item_number=open_item,
                        question_type="certo_errado",
                        question_text=" ".join(context).strip(),
                        item_text=text,
                        source_type=doc.source_type,
                        source_file=doc.source_file,
                    )
                )
                context.clear()
            open_item = None
            open_item_lines = []

        for ln in lines[start:]:
            s = ln.strip()
            if not s:
                continue
            head = is_section_header(s)
            if head:
                close_item()
                discipline = normalize_disc(head)
                expected_next = (
                    1 if expected_next == 1 else expected_next
                )  # numeracao continua
                continue
            if HEADER_NOISE.search(s) and len(s) < 80 and not open_item:
                close_item()
                context.clear()
                continue

            # item com numero inline?
            m = RE_ITEM_INLINE.match(s)
            if m and int(m.group(1)) == expected_next:
                close_item()
                open_item = int(m.group(1))
                open_item_lines = [m.group(2)]
                expected_next += 1
                continue
            # numero solto na linha?
            m2 = RE_ITEM_ALONE.match(s)
            if m2 and int(m2.group(1)) == expected_next:
                close_item()
                open_item = int(m2.group(1))
                open_item_lines = []
                expected_next += 1
                continue
            # numero solto seguido de texto (numero ficou na linha anterior do bloco)
            if open_item is not None:
                open_item_lines.append(s)
            else:
                context.append(s)

        close_item()
        exam.questions = rows
        if not rows:
            exam.warnings.append("nenhum item extraido")
        return exam
