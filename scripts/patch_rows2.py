# -*- coding: utf-8 -*-
"""Patch: parse_row_grid para gabaritos CESPE tabulados (2003 e 2006/2007)."""

from pathlib import Path

p = Path("parser/answer_merger.py")
t = p.read_text(encoding="utf-8")

new_fn = '''

RE_ROW_LONG = re.compile(r"^\\s*(\\d{1,3})\\s+((?:[CEX#]\\s*){10,})$")
RE_ROW_SHORT = re.compile(r"^\\s*(\\d{1,3})\\s+((?:[A-E#]\\s*){2,8})$")
RE_NUM_LINE = re.compile(r"^\\s*(\\d{1,3})\\s*$")


def parse_row_grid(text: str) -> tuple[dict, list[str]]:
    """Linhas 'numero + sequencia de letras' em gabaritos CESPE tabulados.

    (a) 2003: linha 'item N + >=10 letras' (letra[j] = resposta da questao
        j do run ascendente 1..N coletado fora das linhas).
    (b) 2006/2007: linha 'item N + 2..8 letras' (coluna = caderno; 1a letra
        = caderno ALFA). Chave = item puro.
    """
    warns: list[str] = []
    long_rows: dict[int, list[str]] = {}
    short_rows: dict[int, list[str]] = {}
    plain_nums: list[int] = []
    for ln in text.split("\\n"):
        s = ln.strip()
        if not s:
            continue
        m_long = RE_ROW_LONG.match(s)
        if m_long:
            long_rows[int(m_long.group(1))] = [
                c for c in m_long.group(2).split() if c in ("C", "E")
            ]
            continue
        m_num = RE_NUM_LINE.match(s)
        if m_num and 1 <= int(m_num.group(1)) <= 200:
            plain_nums.append(int(m_num.group(1)))
            continue
        m_short = RE_ROW_SHORT.match(s)
        if m_short:
            n = int(m_short.group(1))
            toks = m_short.group(2).split()
            if 1 <= n <= 200 and toks:
                short_rows.setdefault(n, toks)

    # (a) 2003-style
    if long_rows and len(plain_nums) >= 10:
        run = _longest_ascending_run(plain_nums)
        if len(run) >= 10:
            out: dict = {}
            item_ns = sorted(long_rows.keys())
            for qn in run:
                idx = qn - run[0]
                for item_n in item_ns:
                    ls = long_rows[item_n]
                    if 0 <= idx < len(ls) and ls[idx] in ("C", "E"):
                        out[(qn, item_n)] = ls[idx]
            if len(out) >= 20:
                return out, warns + [f"row-grid-2003 ({len(out)} pares)"]

    # (b) 2006/2007
    if len(short_rows) >= 20:
        out_b: dict = {}
        for n, toks in short_rows.items():
            if toks[0] in ("C", "E"):
                out_b[n] = toks[0]
        if len(out_b) >= 20:
            return out_b, warns + [f"row-caderno ({len(out_b)} itens)"]
    return {}, warns
'''

if "def parse_row_grid" not in t:
    i = t.index("def merge_answers")
    t = t[:i] + new_fn + "\n\n" + t[i:]

old_ladder = """    # 0.5) linhas "item N + letras" (Cespe 2006/2007 multi-caderno)
    rows, warns_rows = parse_caderno_rows(doc.text)
    if len(rows) >= 20:
        return rows, warns + warns_rows + [f"modo=caderno-rows ({len(rows)} itens)"]"""
new_ladder = """    # 0.5) linhas "item N + letras" (Cespe 2003/2006/2007 tabulados)
    rows, warns_rows = parse_row_grid(doc.text)
    if len(rows) >= 20:
        return rows, warns + warns_rows + [f"modo=row-grid ({len(rows)} pares)"]"""
if old_ladder in t:
    t = t.replace(old_ladder, new_ladder)

p.write_text(t, encoding="utf-8")
import ast

ast.parse(t)
print("patch ok")
