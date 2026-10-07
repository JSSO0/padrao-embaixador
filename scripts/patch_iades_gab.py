# -*- coding: utf-8 -*-
"""Patch: parse_iades_gabarito dedicado (marcadores -> grupos de numeros -> letras)."""

from pathlib import Path

p = Path("parser/answer_merger.py")
t = p.read_text(encoding="utf-8")

new_fn = '''

def parse_iades_gabarito(text: str) -> tuple[dict, list[str]]:
    """IADES 2019-2023 (e 2017 no mesmo padrao): por bloco de questoes,
    a sequencia e: QUESTAO q1, q2, ..., qk (marcadores) -> numeros de itens
    (1..m, 1..m, ... k grupos) -> corrida de letras C/E (k*m).

    Pareia: grupo gi de numeros <-> marcador gi, consumindo letras em fila.
    '#' = item sem gabarito (mantem alinhamento, nao grava).
    """
    warns: list[str] = []
    clean = "\\n".join(ln for ln in text.split("\\n") if not FOOTER_LINE.search(ln))
    events: list[tuple[str, object]] = []
    for m in RE_TOKEN.finditer(clean):
        if m.group(1) is not None:
            events.append(("q", int(m.group(1))))
        elif m.group(2) is not None:
            events.append(("n", int(m.group(2))))
        else:
            events.append(("l", m.group(3).upper()))

    pending_qs: list[int] = []
    groups: list[list[int]] = []
    letters: list[str] = []
    seen_q = False

    for kind, val in events:
        if kind == "q":
            seen_q = True
            pending_qs.append(val)
        elif kind == "n":
            if not seen_q:
                continue  # numeros antes do primeiro marcador = noise
            if val == 1 and groups and groups[-1]:
                groups.append([])
            elif val == 1 and not groups:
                groups.append([])
            if groups:
                if not groups[-1] or val == groups[-1][-1] + 1:
                    groups[-1].append(val)
                # numero fora de sequencia (noise) -> ignora
        elif kind == "l":
            if seen_q:
                letters.append(val)

    out: dict = {}
    li = 0
    for gi, grp in enumerate(groups):
        qn = pending_qs[gi] if gi < len(pending_qs) else None
        for n in grp:
            if li >= len(letters):
                break
            l = letters[li]
            li += 1
            if l in ("C", "E"):
                out[(qn, n)] = l
    if len(out) < 20:
        return {}, warns
    return out, warns + [f"iades-blocos ({len(out)} pares, {len(groups)} grupos)"]
'''

if "def parse_iades_gabarito" not in t:
    i = t.index("def merge_answers")
    t = t[:i] + new_fn + "\n\n" + t[i:]

# integra na escada antes do posicional
old = """    # 1) posicional por corridas (IADes 2019-2023 e Cespe 2003-2016 tabelados)
    pos, warns_p = parse_positional_runs(doc.text)
    if len(pos) >= 20:"""
new = """    # 1) blocos IADES/2017 (QUESTAO N -> numeros 1..k -> letras)
    iades, warns_i = parse_iades_gabarito(doc.text)
    if len(iades) >= 20:
        return iades, warns + warns_i + [f"modo=iades-blocos ({len(iades)} pares)"]

    # 2) posicional por corridas (Cespe 2003-2016 tabelados)
    pos, warns_p = parse_positional_runs(doc.text)
    if len(pos) >= 20:"""
t = t.replace(old, new)

p.write_text(t, encoding="utf-8")
import ast

ast.parse(t)
print("patch ok")
