"""Extrai as provas objetivas (primeira fase) do CACD 2015-2018 para JSONL.

Gera arquivos no mesmo formato das transcrições manuais usadas até 2014
(ex.: data/raw/CACD_2014/cursocacd/cacd_2014_primeira_fase_prova_objetiva_1.md):
um objeto JSON por item, com question_text + item_text.

Estratégia (layout-aware, via pymupdf):
  - cada página tem 2 colunas; linhas reconstruídas por spans com posição
  - classifica cada linha: cabecalho de pagina (descarta), QUESTÃO N (7pt),
    número de item (9pt, margem), número de linha do texto (5.2pt, descarta),
    citação (6pt), corpo (10pt)
  - textos-base ("passages") são identificados por números de linha na margem
    (sequência 1,4,7,...), por parágrafos indentados e por títulos
    ("Texto II"); marcadores "Texto para as questões N [e M]" vinculam o
    texto às questões
  - textos que continuam em colunas/páginas seguintes são emendados pela
    sequência dos números de linha (+3), com desempate pelo texto aberto
    mais antigo

Uso:
    python pipeline/extract_objetivas_2015_2018.py             # extrai tudo
    python pipeline/extract_objetivas_2015_2018.py --year 2015
    python pipeline/extract_objetivas_2015_2018.py --debug     # diagnóstico
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from parser.parsers.base import DISCIPLINE_NORMALIZE, normalize_disc  # noqa: E402

RAW = ROOT / "data" / "raw"

SECTION_ALLOWLIST = set(DISCIPLINE_NORMALIZE) | {
    "RASCUNHO",
    "ESPAÇO LIVRE",
    "ESPACO LIVRE",
}
STOP_SECTIONS = {"RASCUNHO", "ESPAÇO LIVRE", "ESPACO LIVRE"}

RE_QUESTAO = re.compile(r"QUEST[ÃA]O\s+(\d{1,3})\s*$", re.I)
RE_QUESTAO_FULL = re.compile(r"QUEST[ÃA]O\s+\d{1,3}\s*$", re.I)
RE_MARKER = re.compile(
    r"(?:Textos?|Texts?)\s+\d+\s+para responder às quest[õo]es\s+(.+)"
    r"|(?:Textos?|Texts?)\s+\d+\s+to answer questions from\s+(.+)"
    r"|Textos? para (?:as |the )?quest[õo][eé]?s?\s+(.+)"
    r"|Texts? for questions\s+(.+)",
    re.I,
)
RE_TEXTO_TITLE = re.compile(r"^Textos?\s+[IVXLC]+\.?\s*$", re.I)
RE_PAGE_HEADER = re.compile(
    r"\|\|.*\|\||CESPE\s*\||Cespe\s*\|"
    r"|SECRET[ÁÃÀA]RI[OA]S?\s+DA\s+CARREIRA\s+DE\s+DIPLO"
    r"|CARREIRA\s+DE\s+DIPLOMATA\s*[-–|]",
    re.I,
)
RE_PAGE_FOOTER = re.compile(
    r"P[ÁÃÀA]GINA|CONCURSO|SECRET[ÁÃÀA]RIO|TIPO\s|CARREIRA\s+DE\s+DIPLOMATA", re.I
)
RE_AREA_LIVRE = re.compile(
    r"^[ÁÃÀA]rea\s+[Ll]ivre\s*$|^[Ee]spa[ÇCc]o\s+[Ll]ivre\s*$", re.I
)
RE_ITENS_HEADER = re.compile(r"^Itens\s+de\s+\d+\s+a\s+\d+\s*\.?\s*$", re.I)
RE_PROVA_TITLE = re.compile(r"^PROVA\s+OBJETIVA", re.I)
HYPHEN_FIX = re.compile(r"(\w)-\s+(?=\w)")


# --------------------------------------------------------------------------- #
# Modelos
# --------------------------------------------------------------------------- #
@dataclass
class Line:
    page: int  # 1-based
    col: int
    y: float
    x: float
    size: float
    kind: str  # questao | body | cite | linenum
    value: int | None  # numero da questao ou do numero-de-linha
    item: int | None  # numero de item (quando a linha abre um item)
    text: str
    indented: bool = False
    at_margin: bool = False  # linha alinhada a margem (enunciado/marcador)


@dataclass
class Segment:
    """Trecho de texto-base coletado entre fronteiras (questao/item/marcador)."""

    lines: list[tuple] = field(default_factory=list)  # (page,col,y,indented,text)
    linenums: list[int] = field(default_factory=list)
    cites: list[str] = field(default_factory=list)
    marker_targets: set[int] | None = None
    owner_q: int | None = None  # questao em cujos itens o trecho apareceu
    owner_phase: str = "pending"  # intro | items | pending
    phys: tuple = (99, 9, 9e9)

    @property
    def first_val(self) -> int | None:
        return self.linenums[0] if self.linenums else None

    @property
    def last_val(self) -> int | None:
        return self.linenums[-1] if self.linenums else None


@dataclass
class Passage:
    segments: list[Segment] = field(default_factory=list)
    marker_targets: set[int] | None = None

    @property
    def last_val(self) -> int | None:
        vals = [s.last_val for s in self.segments if s.last_val is not None]
        return vals[-1] if vals else None

    @property
    def first_phys(self) -> tuple:
        return self.segments[0].phys if self.segments else (99, 9, 9e9)

    def has_cite(self) -> bool:
        return any(s.cites for s in self.segments)

    def text(self) -> str:
        parts: list[str] = []
        for seg in self.segments:
            for page, col, y, indented, txt in seg.lines:
                parts.append(("\n" if indented else " ") + txt)
            if seg.cites:
                parts.append("\n" + " ".join(seg.cites))
        return clean_text("".join(parts))


@dataclass
class QuestionBlock:
    number: int
    page: int
    phys: tuple
    intro: list[tuple] = field(default_factory=list)  # (page,col,y,indented,text)
    intro_cites: list[str] = field(default_factory=list)
    intro_linenums: list[int] = field(default_factory=list)
    items: dict[int, list[tuple]] = field(
        default_factory=dict
    )  # item -> [(page,col,y,indented,text)]
    item_cites: dict[int, list[str]] = field(default_factory=dict)
    discipline: str = ""


RE_FIM_TEXTO = re.compile(r"\s*!FimDoTexto!\s*", re.I)
RE_TRAILING_LABEL = re.compile(
    r"\s+(Espa[çc]o\s+livre|Textos?\s+[IVXLC]+\.?)\s*$", re.I
)


def clean_text(s: str) -> str:
    s = HYPHEN_FIX.sub(r"\1", s)
    s = RE_FIM_TEXTO.sub(" ", s)
    s = RE_TRAILING_LABEL.sub("", s.strip())
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


def join_parts(parts: list[tuple]) -> str:
    """Junta entradas (page,col,y,indented,text): '\n' antes de paragrafo."""
    out: list[str] = []
    for page, col, y, indented, txt in parts:
        if not out:
            out.append(txt)
        else:
            out.append(("\n" if indented else " ") + txt)
    return clean_text("".join(out))


# --------------------------------------------------------------------------- #
# Fase 1: linhas com layout
# --------------------------------------------------------------------------- #
def _column_margin(spans: list[tuple]) -> float:
    """Margem esquerda da coluna = menor x entre numeros pequenos."""
    xs = [s[1] for s in spans if 4.5 <= s[3] <= 9.7 and s[4].strip().isdigit()]
    all_x = min(s[1] for s in spans) if spans else 28.0
    m = min(xs) if xs else all_x
    return m if m - all_x < 12 else all_x


def find_gutter(spans: list[tuple], pw: float) -> float | None:
    """Detecta o corte vertical entre 2 colunas: menor vao valido sem span
    cruzando (o menor corte mantem os numeros de margem na sua coluna)."""


def find_gutter(spans: list[tuple], pw: float) -> float | None:
    """Detecta o corte vertical entre 2 colunas: menor vao valido sem span
    cruzando. Spans de largura unica (capa/rodape) sao excluidos do teste,
    pois cruzam qualquer corte."""
    body = [s for s in spans if (s[2] - s[1]) <= FW_WIDTH * pw]
    lefts = sorted({round(s[2], 1) for s in body if s[2] <= 0.55 * pw})  # x1
    rights = sorted({round(s[1], 1) for s in body if s[1] >= 0.45 * pw})  # x0
    for lx in lefts:
        for rx in rights:
            if rx - lx < 4 or not (lx < 0.5 * pw < rx):
                continue
            cut = (lx + rx) / 2
            if any(s[1] < cut < s[2] for s in body):
                continue
            n_left = len([s for s in body if s[2] <= cut])
            n_right = len([s for s in body if s[1] >= cut])
            if n_left >= 4 and n_right >= 1:
                return cut
    return None


FW_WIDTH = 0.55  # fracao da largura da pagina que caracteriza linha full-width
ZONE_TOL = 26.0  # pt acima da 1a linha full-width para pegar o cabecalho


def _merge_zones(ys: list[float], tol: float = 30.0) -> list[tuple[float, float]]:
    """Agrupa y's em zonas contiguas."""
    if not ys:
        return []
    ys = sorted(ys)
    zones = [[ys[0], ys[0]]]
    for y in ys[1:]:
        if y - zones[-1][1] <= tol:
            zones[-1][1] = y
        else:
            zones.append([y, y])
    return [(a, b) for a, b in zones]


def extract_lines(pdf_path: Path) -> list[Line]:
    pdf = pymupdf.open(pdf_path)
    lines: list[Line] = []
    for pno, page in enumerate(pdf, start=1):
        pw = page.rect.width
        spans = []
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if s["text"].strip():
                        spans.append(
                            (
                                s["bbox"][1],
                                s["bbox"][0],
                                s["bbox"][2],
                                s["size"],
                                unicodedata.normalize("NFC", s["text"]),
                            )
                        )
        # cabecalhos de pagina, titulos de prova e rodape
        spans = [s for s in spans if not (s[0] < 48 and RE_PAGE_HEADER.search(s[4]))]
        spans = [s for s in spans if not (s[0] >= 790 and RE_PAGE_FOOTER.search(s[4]))]
        spans = [s for s in spans if not RE_PROVA_TITLE.match(s[4].strip())]

        # titulos de secao (fonte grande) viram eventos proprios no topo
        titles = [s for s in spans if s[3] >= 12.0]
        body = [s for s in spans if s[3] < 12.0]

        # sequencia de bandas: title | cols | single | cols | single ...
        seq: list[tuple[str, list[tuple]]] = []
        if titles:
            seq.append(("title", titles))
        fw_ys = [s[0] for s in body if (s[2] - s[1]) > FW_WIDTH * pw]
        zones = [(a - ZONE_TOL, b + 20.0) for a, b in _merge_zones(fw_ys)]
        buf: list[tuple] = []
        last_zone: int | None = None
        for s in sorted(body, key=lambda s: s[0]):
            y = s[0]
            zi = next((i for i, (a, b) in enumerate(zones) if a <= y <= b), None)
            if zi != last_zone:
                if buf:
                    seq.append(("cols" if last_zone is None else "single", buf))
                    buf = []
                if zi is not None and (not seq or seq[-1][0] != "single"):
                    seq.append(("single", []))
                last_zone = zi
            buf.append(s)
        if buf:
            seq.append(("cols" if last_zone is None else "single", buf))

        col_idx = 0
        for kind, grp in seq:
            if not grp:
                continue
            if kind in ("title", "single"):
                lines.extend(
                    _classify_column(
                        grp, col_idx, pno, _column_margin(grp), multi=False
                    )
                )
                col_idx += 1
            else:
                cut = find_gutter(grp, pw)
                if cut is None:
                    lines.extend(
                        _classify_column(
                            grp, col_idx, pno, _column_margin(grp), multi=False
                        )
                    )
                    col_idx += 1
                else:
                    left = [s for s in grp if s[2] <= cut]
                    right = [s for s in grp if s[1] >= cut]
                    if left:
                        lines.extend(
                            _classify_column(
                                left, col_idx, pno, _column_margin(left), multi=True
                            )
                        )
                    if right:
                        lines.extend(
                            _classify_column(
                                right,
                                col_idx + 1,
                                pno,
                                _column_margin(right),
                                multi=True,
                            )
                        )
                    col_idx += 2
    pdf.close()
    lines.sort(key=lambda l: (l.page, l.col, l.y))
    return lines


def _classify_column(
    spans: list[tuple], col: int, pno: int, col_margin: float, multi: bool
) -> list[Line]:
    # separa numeros de margem (item ~10pt / linha 5-6.5pt) do conteudo
    margin_nums: list[tuple] = []
    content: list[tuple] = []
    for s in spans:
        y, x, x1, sz, t = s
        if sz <= 10.5 and t.strip().isdigit() and x <= col_margin + 20:
            margin_nums.append(s)
        else:
            content.append(s)

    # agrupa conteudo em linhas por faixa de y (tolerancia 3.5pt)
    content.sort(key=lambda s: (s[0], s[1]))
    groups: list[list] = []
    for s in content:
        if groups and abs(groups[-1][0][0] - s[0]) <= 3.5:
            groups[-1].append(s)
        else:
            groups.append([s])

    lines: list[Line] = []
    for g in groups:
        y = min(s[0] for s in g)
        size = max(s[3] for s in g)
        x = min(s[1] for s in g)
        text = "".join(s[4] for s in sorted(g, key=lambda s: s[1]))
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue

        kind, value, item = "body", None, None
        if RE_QUESTAO_FULL.match(text):
            kind = "questao"
            value = int(RE_QUESTAO.search(text).group(1))
        elif size <= 8.5:
            kind = "cite"
        indented = multi and kind == "body" and size >= 9.8 and (x - col_margin) > 33
        at_margin = kind == "body" and (x - col_margin) <= 10
        if kind == "body":
            # pareia com numero de item da margem (mesma linha visual, <=8pt)
            best = None
            for s0 in margin_nums:
                my, msz, mt = s0[0], s0[3], s0[4]
                if msz < 8.0 or abs(my - y) > 8:
                    continue
                if best is None or abs(my - y) < abs(best[0] - y):
                    best = s0
            if best is not None:
                item = int(best[4].strip())
                margin_nums.remove(best)
        lines.append(
            Line(
                page=pno,
                col=col,
                y=round(y, 1),
                x=round(x, 1),
                size=round(size, 1),
                kind=kind,
                value=value,
                item=item,
                text=text,
                indented=indented,
            )
        )

    # numeros de margem nao pareados (numeros de linha do texto-base)
    for my, mx, _mx1, msz, mt in margin_nums:
        t = mt.strip()
        if msz <= 7.5 and t.isdigit():
            lines.append(
                Line(
                    pno,
                    col,
                    round(my, 1),
                    round(mx, 1),
                    msz,
                    "linenum",
                    int(t),
                    None,
                    "",
                )
            )
    lines.sort(key=lambda l: l.y)
    return lines


# --------------------------------------------------------------------------- #
# Fase 2: blocos
# --------------------------------------------------------------------------- #
def parse_marker_targets(text: str) -> set[int]:
    m = RE_MARKER.search(text)
    tail = ""
    if m:
        for g in m.groups():
            if g:
                tail = g
                break
    else:
        tail = text
    nums = [int(n) for n in re.findall(r"\d+", tail)]
    if len(nums) >= 2 and re.search(r"\s+a\s+|\s+and\s+|\s+to\s+|\s+e\s+", tail, re.I):
        return set(range(nums[0], nums[-1] + 1))
    return set(nums)


def build_blocks(lines: list[Line], individual: bool = False):
    blocks: list = []  # ("section", nome) | ("marker", targets, phys) | QuestionBlock | Segment
    section_buf: list[Line] = []
    discipline = ""
    q: QuestionBlock | None = None
    cur_item: int | None = None
    seg: Segment | None = None
    marker_pending: set[int] | None = None
    rascunho = False
    last_real_disc = ""

    def close_segment():
        nonlocal seg
        if seg is not None and (seg.lines or seg.cites):
            blocks.append(seg)
        seg = None

    def close_question():
        nonlocal q, cur_item
        if q is not None:
            q.discipline = discipline
            blocks.append(q)
        q = None
        cur_item = None

    def open_seg(ln: Line):
        nonlocal seg, marker_pending
        if q is None:
            phase = "pending"
        elif cur_item is None:
            phase = "intro"
        else:
            phase = "items"
        seg = Segment(marker_targets=marker_pending, owner_q=q.number if q else None)
        seg.owner_phase = phase
        marker_pending = None
        seg.phys = (ln.page, ln.col, ln.y)
        return seg

    def seg_add(txt: str, page: int, col: int, y: float, indented: bool, cite: bool):
        nonlocal seg
        if seg is None:
            open_seg(Line(page, col, y, 0.0, 10.0, "body", None, None, txt))
            seg.phys = (page, col, y)
        if cite:
            seg.cites.append(txt)
        else:
            seg.lines.append((page, col, y, indented, txt))

    def handle_body(ln: Line):
        nonlocal seg, marker_pending
        if discipline == "":
            return  # capa/instrucoes antes da primeira disciplina
        # marcador "Texto para as questoes N e M"
        if ln.kind == "body" and RE_MARKER.search(ln.text):
            close_segment()
            close_question()  # marcador entre questoes: fecha a anterior
            marker_pending = parse_marker_targets(ln.text)
            blocks.append(("marker", marker_pending, (ln.page, ln.col, ln.y)))
            return
        # titulo "Texto II"
        if ln.kind == "body" and RE_TEXTO_TITLE.search(ln.text):
            close_segment()
            open_seg(ln)
            seg.lines.append((ln.page, ln.col, ln.y, True, ln.text))
            return
        if ln.kind == "cite":
            if seg is not None:
                seg_add(ln.text, ln.page, ln.col, ln.y, False, True)
            elif q is not None and cur_item is not None:
                q.item_cites.setdefault(cur_item, []).append(ln.text)
            elif q is not None:
                q.intro_cites.append(ln.text)
            else:
                seg_add(ln.text, ln.page, ln.col, ln.y, False, True)
            return
        # corpo normal
        if (
            seg is not None
            and q is not None
            and cur_item is None
            and ln.at_margin
            and not (individual and "julg" not in ln.text.lower())
        ):
            close_segment()  # enunciado na margem apos o texto-base: encerra o texto
        if (
            ln.indented
            and q is not None
            and seg is None
            and (cur_item is not None or individual)
        ):
            open_seg(ln)  # paragrafo indentado no meio dos itens = novo texto
        if seg is not None:
            seg_add(ln.text, ln.page, ln.col, ln.y, ln.indented, False)
            return
        if q is None:
            seg_add(ln.text, ln.page, ln.col, ln.y, ln.indented, False)
            return
        if cur_item is None:
            q.intro.append((ln.page, ln.col, ln.y, ln.indented, ln.text))
        elif cur_item in q.items:
            q.items[cur_item].append((ln.page, ln.col, ln.y, ln.indented, ln.text))

    for ln in lines:
        # ---- rotulos de area de rascunho e cabecalhos "Itens de N a M": lixo ----
        if ln.kind == "body" and (
            RE_AREA_LIVRE.match(ln.text.strip())
            or RE_ITENS_HEADER.match(ln.text.strip())
        ):
            continue
        # ---- modo rascunho: ignora conteudo ate surgir questao/item novo ----
        if rascunho and ln.kind not in ("questao",) and ln.item is None:
            continue
        if rascunho:
            rascunho = False
            discipline = last_real_disc
        # ---- secoes (linhas caps acumuladas) ----
        big = (
            ln.kind == "body"
            and 10.6 <= ln.size < 12.5
            and ln.text.strip().upper() in SECTION_ALLOWLIST
        )
        if big:
            close_segment()
            close_question()
            section_buf = []
            blocks.append(("section", ln.text.strip()))
            discipline = normalize_disc(ln.text)
            continue
        caps = (
            ln.kind == "body"
            and ln.text == ln.text.upper()
            and len(ln.text) >= 4
            and not ln.text.isdigit()
            and not RE_MARKER.search(ln.text)
        )
        if caps:
            trial = " ".join([b.text for b in section_buf] + [ln.text]).strip()
            if trial.upper() in SECTION_ALLOWLIST:
                close_segment()
                close_question()
                section_buf = []
                blocks.append(("section", trial))
                if trial.upper() in STOP_SECTIONS:
                    rascunho = True
                    discipline = last_real_disc
                else:
                    discipline = normalize_disc(trial)
                    last_real_disc = discipline
                continue
            if len(section_buf) < 3:
                section_buf.append(ln)
                continue
            # estourou: emite o acumulado como corpo e trata a linha atual
            acc = section_buf[0]
            section_buf = [ln]
            handle_body(acc)
            continue
        if section_buf:
            acc = section_buf[0]
            section_buf = []
            handle_body(acc)

        # ---- capa/instrucoes antes da primeira disciplina: descarta ----
        if discipline == "":
            continue

        # ---- eventos estruturais ----
        if ln.kind == "questao":
            close_segment()
            close_question()
            q = QuestionBlock(
                number=ln.value, page=ln.page, phys=(ln.page, ln.col, ln.y)
            )
            continue
        if ln.item is not None:
            close_segment()
            if individual:
                # formato 2025/2026: cada numero impresso e uma questao
                # (comando proprio, sem itens agrupados)
                close_question()
                q = QuestionBlock(
                    number=ln.item, page=ln.page, phys=(ln.page, ln.col, ln.y)
                )
                # a propria linha e o inicio do comando (question_text)
                q.intro.append((ln.page, ln.col, ln.y, ln.indented, ln.text))
                continue
            if q is not None:
                cur_item = ln.item
                q.items[cur_item] = []
                # a propria linha e o primeiro texto do item
                q.items[cur_item].append((ln.page, ln.col, ln.y, ln.indented, ln.text))
            continue
        if ln.kind == "linenum":
            if seg is None and (q is None or cur_item is not None):
                # primeiro numero de linha neste contexto: abre texto-base
                open_seg(ln)
            if seg is not None:
                seg.linenums.append(ln.value)
            elif q is not None:
                q.intro_linenums.append(ln.value)
            continue
        handle_body(ln)

    close_segment()
    close_question()
    return blocks


# --------------------------------------------------------------------------- #
# Fase 3: montagem (passages + questoes)
# --------------------------------------------------------------------------- #
def assemble(blocks: list):
    questions = [b for b in blocks if isinstance(b, QuestionBlock)]
    passages: list[Passage] = []
    open_passages: list[Passage] = []
    marker_pending: set[int] | None = None
    warnings: list[str] = []

    def new_passage(seg: Segment) -> Passage:
        p = Passage(marker_targets=seg.marker_targets)
        p.segments.append(seg)
        passages.append(p)
        open_passages.append(p)
        return p

    q_by_num = {q.number: q for q in questions}
    for b in blocks:
        if isinstance(b, tuple) and b and b[0] == "marker":
            marker_pending = b[1]
            continue
        if not isinstance(b, Segment):
            continue
        fv = b.first_val
        # texto-base aberto durante o enunciado da propria questao: anexa ao intro
        if b.owner_q and b.owner_phase == "intro" and not b.marker_targets:
            owner = q_by_num.get(b.owner_q)
            if owner is not None:
                owner.intro.extend(b.lines)
                owner.intro_cites.extend(b.cites)
                continue
        if fv is None or fv == 1 or b.marker_targets is not None:
            new_passage(b)
            continue
        # continuacao: procura texto aberto compativel (marcador > mais antigo)
        cands = [
            p
            for p in open_passages
            if p.last_val is not None and 0 < fv - p.last_val <= 6
        ]
        cands.sort(key=lambda p: (p.marker_targets is None, passages.index(p)))
        if cands:
            cands[0].segments.append(b)
            if b.cites:  # texto completo
                open_passages.remove(cands[0])
            continue
        # continuacao do texto do proprio enunciado (passagem inline)
        owner = q_by_num.get(b.owner_q) if b.owner_q else None
        if (
            owner is not None
            and owner.intro_linenums
            and 0 < fv - owner.intro_linenums[-1] <= 6
        ):
            owner.intro.extend(b.lines)
            owner.intro_cites.extend(b.cites)
            continue
        warnings.append(f"continuacao sem origem: linenum {fv} @ {b.phys}")
        new_passage(b)

    # marcador sem texto novo depois dele: vincula o texto aberto mais recente
    bound: dict[int, Passage] = {}
    for p in passages:
        if p.marker_targets:
            tgt = min(p.marker_targets)
            if tgt in bound:
                warnings.append(f"questao {tgt} recebeu 2 textos")
            bound[tgt] = p

    # passages sem vinculo: proxima questao fisicamente depois do texto
    used = set(bound)
    unbound = [p for p in passages if not p.marker_targets]
    unbound.sort(key=lambda p: p.first_phys)
    for p in unbound:
        cand = [
            qn for qn in questions if qn.number not in used and qn.phys > p.first_phys
        ]
        cand.sort(key=lambda qn: qn.phys)
        if cand:
            bound[cand[0].number] = p
            used.add(cand[0].number)
        else:
            warnings.append(f"texto sem questao destino @ {p.first_phys}")

    return questions, passages, bound, warnings


# --------------------------------------------------------------------------- #
# Saida
# --------------------------------------------------------------------------- #
def make_record(
    q: QuestionBlock,
    item: int | None,
    question_text: str,
    item_text: str | None,
    year: int,
    contest: str,
    source_file: str,
) -> dict:
    return {
        "contest_id": contest,
        "year": year,
        "phase": 1,
        "stage": "primeira_fase",
        "discipline": q.discipline or None,
        "question_number": q.number,
        "item_number": item,
        "question_type": "certo_errado",
        "question_text": question_text,
        "item_text": item_text,
        "alternatives": None,
        "answer": None,
        "page": q.page,
        "caderno": None,
        "source_file": source_file,
        "source_url": None,
        "confidence": 0.95,
        "notes": None,
    }


def extract_pdf(pdf_path: Path, debug: bool = False):
    contest = pdf_path.relative_to(RAW).parts[0]
    year = int(contest.replace("CACD_", "").split("_")[0])
    source_file = str(pdf_path.relative_to(ROOT)).replace("\\", "/")

    lines = extract_lines(pdf_path)
    individual = not any(l.kind == "questao" for l in lines)
    blocks = build_blocks(lines, individual=individual)
    questions, passages, bound, warnings = assemble(blocks)

    records = []
    for q in questions:
        p = bound.get(q.number)
        intro = join_parts(q.intro)
        if q.intro_cites:
            intro = (intro + "\n" + "\n".join(q.intro_cites)).strip()
        question_text = (p.text() + "\n" + intro).strip() if p else intro
        if not q.items:
            # formato 2025/2026 (item individual com comando proprio)
            records.append(
                make_record(q, None, question_text, None, year, contest, source_file)
            )
            continue
        for item in sorted(q.items):
            item_text = join_parts(q.items[item])
            if q.item_cites.get(item):
                item_text = (item_text + "\n" + " ".join(q.item_cites[item])).strip()
            records.append(
                make_record(
                    q, item, question_text, item_text, year, contest, source_file
                )
            )
    if debug:
        n_items = [len(q.items) for q in questions]
        print(f"--- {pdf_path.name}")
        print(
            f"  questoes: {len(questions)} | itens: {sum(n_items)} | "
            f"itens/questao: {dict(sorted(Counter(n_items).items()))}"
        )
        print(f"  disciplinas: {dict(Counter(q.discipline for q in questions))}")
        print(f"  textos: {len(passages)} | vinculados: {len(bound)}")
        for w in warnings:
            print("  warn:", w)
        for q in questions[:2]:
            p = bound.get(q.number)
            print(
                f"  Q{q.number} [{q.discipline}] pg{q.page} texto={'sim' if p else 'nao'}"
            )
            print("    qt:", (question_text or "")[:150].replace(chr(10), " / "))
    return records, warnings


def find_provas(edition: str) -> list[Path]:
    hits = sorted((RAW / f"CACD_{edition}").glob("*/prova_objetiva*.pdf"))
    if not hits:
        raise FileNotFoundError(f"provas objetivas nao encontradas em CACD_{edition}")

    # ordena pelo menor numero de questao/item impresso (prova 1 antes da 2)
    def min_qn(p: Path) -> int:
        import pymupdf

        with pymupdf.open(p) as doc:
            text = "\n".join(pg.get_text("text") for pg in doc)
        nums = [int(m.group(1)) for m in re.finditer(r"Quest[ÃA]O\s+(\d+)", text, re.I)]
        # formato 2025/2026: numeros de item soltos (linhas puramente numericas)
        nums += [int(m.group(0)) for m in re.finditer(r"^\s*(\d{1,3})\s*$", text, re.M)]
        return min(nums) if nums else 9999

    # dedup: a mesma prova pode existir em 2 fontes (cebraspe/cursocacd);
    # 1 registro por faixa inicial de questoes, priorizando a pasta cebraspe
    ranked = sorted(
        hits, key=lambda p: (min_qn(p), 0 if p.parent.name == "cebraspe" else 1)
    )
    out: list[Path] = []
    seen: set[int] = set()
    for p in ranked:
        k = min_qn(p)
        if k in seen:
            continue
        seen.add(k)
        out.append(p)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=str, action="append", dest="editions")
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args()
    editions = args.editions or [2015, 2016, 2017, 2018]

    total = 0
    for edition in editions:
        contest = f"CACD_{edition}"
        for part, pdf in enumerate(find_provas(edition), start=1):
            records, warns = extract_pdf(pdf, debug=args.debug)
            out = (
                pdf.parent / f"cacd_{edition}_primeira_fase_prova_objetiva_{part}.jsonl"
            )
            with out.open("w", encoding="utf-8") as f:
                for r in records:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            nq = len([r for r in records if r["item_number"] is not None])
            total += len(records)
            print(f"[ok] {out.relative_to(ROOT)}: {nq} itens")
            for w in warns:
                print(f"     warn: {w}")
    print(f"== total de registros: {total}")


if __name__ == "__main__":
    main()
