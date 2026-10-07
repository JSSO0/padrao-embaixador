"""Parser IADES 2019-2023 (formato certo/errado, itens reiniciam por questao).

Decodificado por inspecao real (docs/inspecao-formatos.md):
  - "QUESTAO N" delimita questoes; numerao dos itens REINICIA em 1 por questao
  - numeros soltos em sequencia com passo 3 (1,4,7,10...) = NUMEROS DE LINHA
    na margem do caderno (noise) — aparecem em clusters no topo de pagina
  - inicio de item = numero solto em linha SEGUIDO de texto
  - headers: disciplina ("Lingua Portuguesa"), "Itens de X a Y", "Espaco livre"
  - layout 2 colunas resolvido pelo loader (cluster_columns)
"""

from __future__ import annotations

import re

from parser.document_loader import LoadedDoc
from parser.models import ParsedExam, Question, question_id
from parser.parsers.base import DocumentParser, RE_QUESTION_MARK, normalize_disc

RE_ITEM_ALONE = re.compile(r"^\s*(\d{1,3})\s*$")
RE_ITEM_INLINE = re.compile(r"^\s*(\d{1,3})\s+(\S.+)$")
RE_HEADER_ITENS = re.compile(r"(?i)Itens de\s+(\d+)\s+a\s+(\d+)")
NOISE_LINE = re.compile(
    r"(?i)^(Espa[çc]o livre|PROVA APLICADA|Caderno de Prova.*|CEBRASPE.*|IADES.*)$"
)
DISCIPLINE_CAPS = re.compile(r"^[A-ZÀ-Ü][A-ZÀ-Ü\s]{3,40}$")


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
        lines = doc.text.split("\n")

        # posicoes dos marcadores QUESTAO N
        marks = list(RE_QUESTION_MARK.finditer(doc.text))
        line_offsets: list[int] = []
        pos = 0
        for ln in lines:
            line_offsets.append(pos)
            pos += len(ln) + 1

        def line_for(offset: int) -> int:
            lo, hi = 0, len(line_offsets) - 1
            while lo < hi:
                mid = (lo + hi) // 2
                if line_offsets[mid] <= offset:
                    lo = mid + 1
                else:
                    hi = mid
            return max(lo - 1, 0)

        rows: list[Question] = []
        warnings: list[str] = []

        for mi, m in enumerate(marks):
            qnum = int(m.group(1))
            s0 = line_for(m.start())
            s1 = (
                line_for(marks[mi + 1].start()) - 1
                if mi + 1 < len(marks)
                else len(lines) - 1
            )
            block = [x.strip() for x in lines[s0 : s1 + 1]]

            discipline = None
            expected_item = 1
            stimulus: list[str] = []
            open_item: int | None = None
            open_lines: list[str] = []
            pending: int | None = None  # numero solto aguardando proxima linha
            consecutive_numbers = 0  # contador de numeros soltos em cadeia (margem)

            def close_item() -> None:
                nonlocal open_item, open_lines
                if open_item is None:
                    return
                text = " ".join(open_lines).strip()
                if text:
                    rows.append(
                        Question(
                            question_id=question_id(
                                doc.contest_id,
                                "primeira_fase",
                                discipline,
                                qnum,
                                open_item,
                            ),
                            parent_question_id=question_id(
                                doc.contest_id, "primeira_fase", discipline, qnum, None
                            ),
                            contest_id=doc.contest_id,
                            year=doc.year,
                            phase=1,
                            stage="primeira_fase",
                            discipline=discipline,
                            question_number=qnum,
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

            for s in block:
                if not s:
                    continue
                if NOISE_LINE.match(s):
                    continue
                if RE_HEADER_ITENS.match(s):
                    # "Itens de 1 a 10" -> confirma contagem esperada
                    expected_item = int(RE_HEADER_ITENS.match(s).group(1))
                    continue
                if (
                    re.match(r"^[A-ZÀ-Ü][a-zà-ü]", s)
                    and s.upper() != s
                    and len(s) < 40
                    and "julgue" not in s.lower()
                ):
                    discipline = normalize_disc(s)  # ex.: "Língua Portuguesa"
                    continue

                m_alone = RE_ITEM_ALONE.match(s)
                m_inline = RE_ITEM_INLINE.match(s)
                if m_alone:
                    n = int(m_alone.group(1))
                    # desambiguacao: numero solto pode ser item (n == esperado e
                    # proxima linha = texto) ou numero de linha da margem (cadeia)
                    if n == expected_item:
                        if open_item is not None:
                            close_item()
                        pending = n
                        expected_item = n + 1
                        continue
                    consecutive_numbers += 1
                    if pending is not None and consecutive_numbers >= 1:
                        # era cadeia de margem: o "item pendente" era numero de linha
                        pending = None
                        stimulus.clear()
                    continue
                if m_inline and int(m_inline.group(1)) == expected_item:
                    close_item()
                    open_item = int(m_inline.group(1))
                    open_lines = [m_inline.group(2)]
                    expected_item += 1
                    pending = None
                    consecutive_numbers = 0
                    continue
                # linha de texto
                if pending is not None:
                    # o numero pendente era o INICIO DE ITEM de verdade
                    open_item = pending
                    open_lines = [s]
                    pending = None
                    consecutive_numbers = 0
                elif open_item is not None:
                    open_lines.append(s)
                else:
                    stimulus.append(s)
            close_item()

        exam = ParsedExam(
            contest_id=doc.contest_id,
            source_file=doc.source_file,
            family=self.family,
            questions=rows,
            warnings=warnings,
        )
        if not rows:
            exam.warnings.append("nenhum item extraido")
        return exam


RE_ITEM_INLINE = re.compile(r"^\s*(\d{1,3})\s+(.+)$")
RE_ITEM_ALONE = re.compile(r"^\s*(\d{1,3})\s*$")


def normalize_disc(raw: str) -> str:
    from parser.parsers.base import normalize_disc as nd

    return nd(raw)
