"""Extracao de gabaritos (regras puras) e fusao com questoes.

Formatos suportados:
  - pares numero + C/E (item certo/errado): "1 C", "1-C", "1. Certo"
  - pares numero + letra (multipla escolha): "1 A 2 C 3 D" ou tabelas
Conflito preliminar x definitivo: definitivo vence (ultimo na lista de keys);
conflitos sao retornados como avisos.
"""

from __future__ import annotations

import re

RE_PAIR_CE = re.compile(
    r"(?<!\d)(\d{1,3})\s*[\.\-–—:)]?\s*(C|E|CERTO|ERRADO)\b(?![A-Za-z])", re.IGNORECASE
)
RE_PAIR_LETTER = re.compile(r"(?<!\d)(\d{1,3})\s*[\.\-–—:)]?\s*([A-E])\b(?![A-Za-z])")
NOISE = re.compile(
    r"(?i)(lista de isen|resultado|convoca|demanda de candidatos|parecer)"
)


def normalize_ce(v: str) -> str:
    v = v.upper()
    return "E" if v.startswith("E") else "C"


def parse_answer_key(
    text: str,
) -> tuple[dict[int, str], dict[int, list[str]], list[str]]:
    """Retorna (pares C/E, pares letra (multiplas leituras), avisos)."""
    warns: list[str] = []
    head = text[:1500]
    if NOISE.search(head) and "gabarito" not in head.lower():
        warns.append("texto pode nao ser gabarito")

    ce: dict[int, str] = {}
    letters_multi: dict[int, list[str]] = {}
    for m in RE_PAIR_CE.finditer(text):
        num = int(m.group(1))
        val = normalize_ce(m.group(2))
        prev = ce.get(num)
        if prev and prev != val:
            warns.append(f"conflito C/E no numero {num}: {prev} vs {val}")
        ce[num] = val

    for m in RE_PAIR_LETTER.finditer(text):
        num = int(m.group(1))
        if num in ce:  # numero ja interpretado como C/E
            continue
        letters_multi.setdefault(num, []).append(m.group(2).upper())

    # deriva a letra final por numero (ultima leitura vence)
    letters: dict[int, str] = {n: ls[-1] for n, ls in letters_multi.items() if ls}
    return ce, letters, warns


def extract_answer_key(doc) -> tuple[dict[int, str], list[str]]:
    """Interpreta um LoadedDoc de gabarito. Retorna (mapa numero->resposta, avisos)."""
    ce, letters, warns = parse_answer_key(doc.text)
    if len(ce) >= len(letters):
        return ce, warns + [f"modo=C/E ({len(ce)} pares)"]
    return letters, warns + [f"modo=letras ({len(letters)} pares)"]


def merge_answers(
    questions: list, answer_keys: list[tuple[str, dict[int, str]]]
) -> list[str]:
    """Casamento por numero (questao MC ou item). Definitivo = ultimo da lista."""
    warns: list[str] = []
    by_num: dict[int, str] = {}
    for name, key in answer_keys:
        for n, v in key.items():
            if n in by_num and by_num[n] != v:
                warns.append(
                    f"conflito de gabarito numero {n}: {by_num[n]} vs {v} ({name})"
                )
            by_num[n] = v
    for q in questions:
        num = (
            q.question_number if q.question_type == "multiple_choice" else q.item_number
        )
        if num is not None and num in by_num:
            ans = by_num[num]
            if q.question_type == "certo_errado" and ans in ("C", "E"):
                q.answer = ans
            elif q.question_type == "multiple_choice" and ans in "ABCDE":
                q.answer = ans
    return warns
