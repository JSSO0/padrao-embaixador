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


def extract_answer_key(doc) -> tuple[dict, list[str]]:
    """Interpreta um LoadedDoc de gabarito. Retorna (mapa -> resposta, avisos).

    Chaves do mapa: int (numero puro) ou tuple (questao, item).
    Estrategia em escada: regex pares -> posicional por corridas -> tabela.
    """
    warns: list[str] = []

    # 0.5) linhas "item N + letras" (Cespe 2003/2006/2007 tabulados)
    rows, warns_rows = parse_row_grid(doc.text)
    if len(rows) >= 20:
        return rows, warns + warns_rows + [f"modo=row-grid ({len(rows)} pares)"]

    # 1) blocos IADES/2017 (QUESTAO N -> numeros 1..k -> letras)
    iades, warns_i = parse_iades_gabarito(doc.text)
    if len(iades) >= 20:
        return iades, warns + warns_i + [f"modo=iades-blocos ({len(iades)} pares)"]

    # 2) posicional por corridas (Cespe 2003-2016 tabelados)
    pos, warns_p = parse_positional_runs(doc.text)
    if len(pos) >= 20:
        return pos, warns + warns_p + [f"modo=posicional ({len(pos)} pares)"]

    # 1.5) grid cespe 2003-style
    grid, warns_g = parse_cespe_grid(doc.text)
    if len(grid) >= 20:
        return grid, warns + warns_g + [f"modo=cespe-grid ({len(grid)} pares)"]

    # 2) regex pares
    ce, letters, warns_r = parse_answer_key(doc.text)
    if len(ce) >= 20 or len(letters) >= 20:
        if len(ce) >= len(letters):
            return ce, warns + warns_r + [f"modo=C/E ({len(ce)} pares)"]
        return letters, warns + warns_r + [f"modo=letras ({len(letters)} pares)"]

    # 3) tabela Cebraspe 2024-2026 (numeros + letras em sequencia)
    tbl, warns_t = parse_cebraspe_table(doc.text)
    return tbl, warns + warns_r + warns_t + [f"modo=tabela ({len(tbl)} pares)"]


RE_TOKEN = re.compile(
    r"QUEST[ÃA]O\s+(\d{1,3})"  # g1: marcador de questao
    r"|(?<!\d)(\d{1,3})(?!\d)"  # g2: numero solto (1-3 digitos)
    r"|(?<![A-Za-z])([CEX#])(?![A-Za-z])",  # g3: letra C/E/X
    re.IGNORECASE,
)
FOOTER_LINE = re.compile(
    r"(?i)(Fone|e-mail|P[áa]gina\s+\d|QE\s+\d|Prova Tipo|Instituto Americano"
    r"| Observa|gabarito alterado|RAZ[ÕO]ES PARA ALTERA)"
)


def parse_positional_runs(text: str) -> tuple[dict, list[str]]:
    """Pareamento posicional: coleta (questao, item) de corridas de numeros e
    pareia com corridas de letras na mesma ordem.

    Casos: (a) IADES: numeros 1..k por QUESTAO + letras corrida (k1 = k2);
           (b) Cespe tabulado: numeros 1..N crescentes + letras = 5*N
               (cada numero de questao recebe k letras consecutivas).
    Retorna dict[(questao|None, item)] = 'C'|'E'.
    """
    warns: list[str] = []
    clean = "\n".join(ln for ln in text.split("\n") if not FOOTER_LINE.search(ln))
    events: list[tuple[str, object]] = []
    for m in RE_TOKEN.finditer(clean):
        if m.group(1) is not None:
            events.append(("q", int(m.group(1))))
        elif m.group(2) is not None:
            events.append(("n", int(m.group(2))))
        else:
            events.append(("l", m.group(3).upper()))

    # agrupa: numero -> questao corrente (ultimo marcador q)
    nums: list[tuple[int | None, int]] = []  # (questao, numero)
    cur_q: int | None = None
    letters: list[str] = []
    for kind, val in events:
        if kind == "q":
            cur_q = val
        elif kind == "n":
            nums.append((cur_q, val))
        else:
            letters.append(val)

    # descarta codas (rodape com muitos 0)
    nums = [(q, n) for (q, n) in nums if 1 <= n <= 300]

    # tentativa IADES: itens sao 1..4 (as vezes 5); filtra numeros altos
    nums_low = [(q, n) for (q, n) in nums if n <= 5]
    low_letters = [l for l in letters if l in ("C", "E")]
    if len(nums_low) == len(low_letters) and len(nums_low) >= 20:
        # agrupa por reinicio em 1: grupo gi ↔ gi-esimo marcador QUESTAO
        qnums = [v for k, v in events if k == "q"]
        groups: list[list[int]] = []
        cur: list[int] = []
        for _, n in nums_low:
            if n == 1 and cur:
                groups.append(cur)
                cur = []
            cur.append(n)
        if cur:
            groups.append(cur)
        out: dict = {}
        for gi, grp in enumerate(groups):
            qn = qnums[gi] if gi < len(qnums) else None
            for j, n in enumerate(grp):
                l = low_letters.pop(0) if low_letters else None
                if l in ("C", "E"):
                    out[(qn, n)] = l
        if len(out) >= 20:
            return out, warns + [
                f"iades-posicional ({len(out)} pares, {len(groups)} grupos)"
            ]

    if len(nums) == len(letters) and len(nums) >= 20:
        # casos (a) e (b)-k=1: pareio direto; questao vem do contexto ou do grupo
        out: dict = {}
        # atribuicao de questao para numeros repetidos (1,2,3,4,1,2,3,4...)
        seq: list[tuple[int | None, int]] = []
        last_num: int | None = None
        for q, n in nums:
            if n == 1 and last_num is not None and last_num != 1:
                cur_q = None  # reinicio de grupo (IADES) — questao ficara sem marcador
            seq.append((cur_q, n))
            last_num = n
        # se todos os nums repetem 1..K, atribui questao sequencial por grupo
        groups: list[list[int]] = []
        cur: list[int] = []
        for _, n in nums:
            if n == 1 and cur:
                groups.append(cur)
                cur = []
            cur.append(n)
        if cur:
            groups.append(cur)
        if len(groups) > 1:
            # contar marcadores QUESTAO para numerar grupos em ordem
            qnums = [v for k, v in events if k == "q"]
            for gi, grp in enumerate(groups):
                qn = qnums[gi] if gi < len(qnums) else None
                for j, n in enumerate(grp):
                    k = letters.pop(0) if letters else None
                    if k in ("C", "E"):
                        out[(qn, n)] = k
            return out, warns + [f"grupos: {len(groups)}"]
        for (q, n), l in zip(nums, letters):
            if l in ("C", "E"):
                out[(q, n)] = l
        return out, warns

    # formato (b): letras == k * numeros (k=2..6), numeros crescentes 1..N
    nums_only = [n for _, n in nums]
    strictly_increasing = (
        all(b == a + 1 for a, b in zip(nums_only, nums_only[1:]))
        and len(nums_only) >= 10
    )
    if strictly_increasing:
        for k in (5, 4, 3, 2):
            if len(letters) == k * len(nums_only):
                out2: dict = {}
                for i, qn in enumerate(nums_only):
                    for j in range(k):
                        l = letters[i * k + j]
                        if l in ("C", "E"):
                            out2[(qn, j + 1)] = l
                return out2, warns + [f"cespe-tabela k={k}: {len(out2)} pares"]
    return {}, warns


def parse_cebraspe_table(text: str) -> tuple[dict[int, str], list[str]]:
    """Gabarito Cebraspe moderno: coluna de numeros + coluna de letras (C/E/X).
    X = item anulado -> nao entra no mapa."""
    warns: list[str] = []
    tokens = text.split()
    nums: list[int] = []
    vals: list[str] = []
    for tok in tokens:
        if re.fullmatch(r"\d{1,3}", tok):
            n = int(tok)
            if 1 <= n <= 300:
                nums.append(n)
        elif tok.upper() in ("C", "E", "X"):
            vals.append(tok.upper())
    out: dict[int, str] = {}
    if len(nums) == len(vals) and len(nums) >= 10:
        anulados = 0
        for n, v in zip(nums, vals):
            if v == "X":
                anulados += 1
                continue
            out[n] = v
        if anulados:
            warns.append(f"{anulados} itens anulados (X)")
    return out, warns




def _longest_ascending_run(nums: list[int]) -> list[int]:
    best: list[int] = []
    cur: list[int] = []
    for n in nums:
        if cur and n != cur[-1] + 1:
            cur = []
        cur.append(n)
        if len(cur) > len(best):
            best = cur
    return best


def parse_cespe_grid(text: str) -> tuple[dict, list[str]]:
    """CESPE 2003-2016 tabulado: header QUESTOES 1..N + k letras por questao.

    Texto extraido: '1 2 3 ... 30' (header), depois linhas de item:
    '1' + k letras, '2' + k letras... (numeros de item 1..k intercalados).
    Aceita tanto nums=[1..N, 1..k] (com headers de linha) quanto so [1..N].
    """
    warns: list[str] = []
    events: list[tuple[str, object]] = []
    for m in RE_TOKEN.finditer(text):
        if m.group(2) is not None:
            events.append(("n", int(m.group(2))))
        elif m.group(3) is not None and m.group(3).upper() in ("C", "E"):
            events.append(("l", m.group(3).upper()))
    letters = [v for k, v in events if k == "l" and v in ("C", "E")]
    nums_all = [v for k, v in events if k == "n" and 1 <= v <= 200]
    if len(letters) < 40:
        return {}, warns
    run = _longest_ascending_run(nums_all := nums_all if False else [v for k, v in events if k == "n"])
    if len(run) < 10:
        return {}, warns
    n_q = len(run)
    for k in (5, 4, 3, 2):
        if len(letters) == k * n_q:
            out: dict = {}
            for i, qn in enumerate(run):
                for j in range(k):
                    l = letters[i * k + j]
                    if l in ("C", "E"):
                        out[(qn, j + 1)] = l
            return out, warns + [f"cespe-grid k={k} ({n_q} questoes)"]
    return {}, warns


def parse_caderno_rows(text: str) -> tuple[dict, list[str]]:
    """CESPE 2006/2007: linhas 'item N + alternativas' (uma letra por caderno;
    itens anulados/universais com '+' ou letra unica). Pega a 1a letra (ALFA).
    """
    warns: list[str] = []
    out: dict = {}
    row = re.compile(r"^\s*(\d{1,3})\s+((?:[CE]\s*){1,6})$")
    for ln in text.split("\n"):
        m = row.match(ln.strip())
        if m:
            item = int(m.group(1))
            first = m.group(2).strip()[0]
            if first in ("C", "E") and 1 <= item <= 200:
                out[item] = first
    if len(out) >= 20:
        warns.append(f"caderno-rows ({len(out)} itens)")
    return out, warns




def parse_iades_gabarito(text: str) -> tuple[dict, list[str]]:
    """IADES 2019-2023 (e 2017 no mesmo padrao): por bloco de questoes,
    a sequencia e: QUESTAO q1, q2, ..., qk (marcadores) -> numeros de itens
    (1..m, 1..m, ... k grupos) -> corrida de letras C/E (k*m).

    Pareia: grupo gi de numeros <-> marcador gi, consumindo letras em fila.
    '#' = item sem gabarito (mantem alinhamento, nao grava).
    """
    warns: list[str] = []
    clean = "\n".join(ln for ln in text.split("\n") if not FOOTER_LINE.search(ln))
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




RE_ROW_LONG = re.compile(r"^\s*(\d{1,3})\s+((?:[CEX#]\s*){10,})$")
RE_ROW_SHORT = re.compile(r"^\s*(\d{1,3})\s+((?:[A-E#]\s*){2,8})$")
RE_NUM_LINE = re.compile(r"^\s*(\d{1,3})\s*$")


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
    for ln in text.split("\n"):
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


RE_QWORD = re.compile(r"^quest[ãa]o$", re.IGNORECASE)
RE_MAT_LETTER = re.compile(r"^[CEX#]$", re.IGNORECASE)
RE_MAT_NUM = re.compile(r"^\d{1,3}$")


def _words_to_rows(
    words: list[tuple[float, float, str]], ytol: float = 3.0
) -> list[tuple[float, list[tuple[float, str]]]]:
    """Agrupa palavras em linhas por proximidade de y (mesma linha da tabela)."""
    ws = sorted(words, key=lambda w: (w[1], w[0]))
    rows: list[tuple[float, list[tuple[float, str]]]] = []
    for x, y, t in ws:
        if rows and abs(y - rows[-1][0]) <= ytol:
            rows[-1][1].append((x, t))
        else:
            rows.append((y, [(x, t)]))
    return [(y, sorted(cells, key=lambda c: c[0])) for y, cells in rows]


def parse_cebraspe_matrix(
    words_per_page: list[list[tuple[float, float, str]]],
) -> tuple[list[dict], list[str]]:
    """Gabarito Cebraspe multi-caderno (2003-2018, 2024).

    Layout: linha de cabecalhos 'Questao N' (N questoes), seguida de uma linha
    com N*k letras (k cadernos). Como as letras estao ordenadas por x e cada
    questao ocupa k colunas consecutivas, a questao i recebe as letras
    letters[i*k:(i+1)*k]; o caderno c e o c-esimo dentro desse grupo.

    Retorna (lista_de_cadernos, avisos); cada caderno e dict {num: 'C'|'E'}.
    'X'/'#' (anulada) nao entram no dict.
    """
    warns: list[str] = []
    cadernos: list[dict] | None = None
    for page in words_per_page:
        if not page:
            continue
        rows = _words_to_rows(page)
        for ri, (_y, cells) in enumerate(rows):
            q_headers: list[tuple[float, int]] = []
            for ci, (x, t) in enumerate(cells):
                if RE_QWORD.match(t):
                    # numero imediatamente a direita
                    for x2, t2 in cells[ci + 1 :]:
                        if RE_MAT_NUM.match(t2):
                            q_headers.append((x, int(t2)))
                            break
            if len(q_headers) < 3:
                continue
            # a linha de respostas deve ser a IMEDIATAMENTE seguinte e conter
            # SO letras (a matriz Cebraspe nao tem linha de numeros de item;
            # o IADES tem, e por isso e' rejeitado aqui)
            if ri + 1 >= len(rows):
                continue
            cells2 = rows[ri + 1][1]
            if not cells2:
                continue
            letters = [(x, t.upper()) for x, t in cells2]
            if not all(RE_MAT_LETTER.match(t) for _x, t in letters):
                continue
            if len(letters) < len(q_headers):
                continue
            n_q = len(q_headers)
            if len(letters) % n_q != 0:
                continue
            k = len(letters) // n_q
            if k < 1 or k > 6:
                continue
            if cadernos is None:
                cadernos = [dict() for _ in range(k)]
            if len(cadernos) != k:
                continue
            for i, (_x, qnum) in enumerate(q_headers):
                for c in range(k):
                    letter = letters[i * k + c][1]
                    if letter in ("C", "E"):
                        cadernos[c][qnum] = letter
    if not cadernos or len(cadernos[0]) < 20:
        return [], warns
    warns.append(f"matriz multi-caderno k={len(cadernos)} ({len(cadernos[0])} questoes)")
    return cadernos, warns


def extract_answer_keys(doc) -> tuple[list[dict], list[str]]:
    """Como extract_answer_key, mas devolve TODOS os cadernos (matriz).

    Caderno 0 = primeira coluna. Se nao for matriz, devolve [chave unica].
    """
    words = getattr(doc, "words_per_page", None)
    if words:
        mats, warns = parse_cebraspe_matrix(words)
        if mats and len(mats[0]) >= 20:
            return mats, warns
    key, warns = extract_answer_key(doc)
    return ([key] if key else []), warns


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
        # chaves candidatas: numero puro e/ou (questao, item)
        if q.question_type == "multiple_choice":
            cands: list = [q.question_number]
        else:
            cands = []
            if q.question_number is not None and q.item_number is not None:
                cands.append((q.question_number, q.item_number))
            if q.item_number is not None:
                cands.append(q.item_number)
        for num in cands:
            if num is not None:
                try:
                    num = int(num)
                except Exception:
                    try:
                        num = int(float(num))
                    except Exception:
                        num = num
            if num is not None and num in by_num:
                ans = by_num[num]
                if q.question_type == "certo_errado" and ans in ("C", "E"):
                    q.answer = ans
                elif q.question_type == "multiple_choice" and ans in "ABCDE":
                    q.answer = ans
                break
    return warns
