# -*- coding: utf-8 -*-
"""Mapa definitivo de secoes por edicao: CABECALHOS CAPS + questoes."""

import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]

SECS = [
    ("língua portuguesa", "Língua Portuguesa"),
    ("língua inglesa", "Língua Inglesa"),
    ("história do brasil", "História do Brasil"),
    ("história mundial", "História Mundial"),
    ("política internacional", "Política Internacional"),
    ("geografia", "Geografia"),
    ("direito internacional público", "Direito"),
    ("direito", "Direito"),
    ("noções de direito", "Direito"),
    ("noções de economia", "Economia"),
    ("economia", "Economia"),
    ("cultura geral", "Cultura Geral"),
]


def sec_de(linha: str) -> str | None:
    t = unicodedata.normalize("NFC", linha).lower().strip()
    for k, v in SECS:
        if t.startswith(k) or k in t[:60]:
            return v
    return None


def mapa_por_caps(f: Path) -> dict[int, str]:
    """Cabecalhos em CAIXA ALTA (CESPE)."""
    t = f.read_text(encoding="utf-8", errors="replace")
    t2 = re.sub(r"[ \t]+", " ", t)
    events = []
    for i, linha in enumerate(t.splitlines()):
        s = linha.strip()
        su = unicodedata.normalize("NFC", s).lower()
        letras = [c for c in s if c.isalpha()]
        caixa_alta = letras and all(c.isupper() for c in letras)
        if 3 < len(s) < 70 and caixa_alta:
            if su.startswith("noções de"):
                v = (
                    "Direito"
                    if "direito" in su
                    else ("Economia" if "economia" in su else None)
                )
                if v:
                    events.append((i, "SEC", v))
                continue
            for k, v in SECS:
                if su == k or (su.startswith(k) and len(su) - len(k) <= 12):
                    events.append((i, "SEC", v))
                    break
        for m in re.finditer(
            r"QUEST.{0,4}O\s+(\d{1,3})", unicodedata.normalize("NFC", s), re.I
        ):
            events.append((i, "Q", int(m.group(1))))
    atual, mapa = None, {}
    for _, tipo, val in sorted(events, key=lambda e: e[0]):
        if tipo == "SEC":
            atual = val
        elif 1 <= val <= 80:
            mapa.setdefault(val, atual)
    return mapa


def mapa_iades(f: Path) -> dict[int, str]:
    """Cabecalho + 'Itens de X a Y' (IADES)."""
    t = unicodedata.normalize("NFC", f.read_text(encoding="utf-8", errors="replace"))
    t = re.sub(r"\s+", " ", t)
    mapa = {}
    for m in re.finditer(r"([A-ZÀ-Úa-zà-ú /]{3,50}?)\s+Itens de (\d+) a (\d+)", t):
        nome = m.group(1).strip()
        sec = None
        for k, v in SECS:
            if k in nome.lower():
                sec = v
                break
        if not sec:
            continue
        for qn in range(int(m.group(2)), int(m.group(3)) + 1):
            mapa[qn] = sec
    return mapa


df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
m1 = df[df.stage.eq("primeira_fase")]

for contest in sorted(m1.contest_id.unique()):
    pasta = ROOT / f"data/processed/text/{contest}"
    provas = sorted(pasta.rglob("prova_objetiva*.txt"))
    if not provas:
        continue
    mapa: dict[int, str] = {}
    for f in provas:
        try:
            mapa.update(mapa_por_caps(f))
            mapa.update(mapa_iades(f))
        except Exception as e:
            print(f"[!!] {f.name}: {e}")
    if not mapa:
        continue
    divs = []
    for qn, sec in sorted(mapa.items()):
        if sec is None:
            continue  # sem secao detectada: nao audita (era TPS / cabecalho ausente)
        sub = m1[m1.contest_id.eq(contest) & m1.question_number.eq(float(qn))]
        if sub.empty:
            continue
        canon = sub.iloc[0]["discipline_canon"]
        if pd.isna(canon) or canon != sec:
            divs.append((qn, sec, canon))
    if divs:
        print(f"--- {contest}: {len(divs)} divergencias (de {len(mapa)} mapeadas)")
        for qn, sec, canon in divs:
            print(f"    q{qn}: secao={sec} | parquet={canon}")
