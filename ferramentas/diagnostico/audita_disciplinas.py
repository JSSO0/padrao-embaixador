# -*- coding: utf-8 -*-
"""Auditoria de disciplinas (M2): mapeia questao -> secao da prova a partir dos
textos extraidos e compara com o discipline_canon do parquet.

Saida: divergencias por edicao (qn, secao da prova, disciplina do parquet).
"""

import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]

SECS = {
    "língua portuguesa": "Língua Portuguesa",
    "língua inglesa": "Língua Inglesa",
    "história do brasil": "História do Brasil",
    "história mundial": "História Mundial",
    "política internacional": "Política Internacional",
    "geografia": "Geografia",
    "noções de direito e direito internacional público": "Direito",
    "noções de direito e de direito internacional": "Direito",
    "direito internacional público": "Direito",
    "noções de economia e de economia internacional": "Economia",
    "noções de economia e de economia internacional e de estatística": "Economia",
    "economia": "Economia",
    "cultura geral": "Cultura Geral",
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s).lower()
    return re.sub(r"\s+", " ", s)


def mapa_secoes(texto: str) -> dict[int, str]:
    t = norm(texto)
    events = []
    for m in re.finditer(
        r"(língua portuguesa|língua inglesa|história do brasil|história mundial"
        r"|política internacional|geografia|noções de direito[^a-z]*pública?"
        r"|noções de direito e de direito internacional"
        r"|noções de economia[^a-z]*internacional|direito internacional público"
        r"|cultura geral)|quest.{0,4}o\s+(\d{1,3})\b",
        t,
    ):
        if m.group(1):
            sec = norm(m.group(1))
            for k, v in SECS.items():
                if k in sec:
                    events.append(("SEC", v))
                    break
        else:
            qn = int(m.group(2))
            if 1 <= qn <= 80:
                events.append(("Q", qn))
    atual = None
    mapa = {}
    for tipo, val in events:
        if tipo == "SEC":
            atual = val
        elif tipo == "Q" and atual:
            mapa.setdefault(val, atual)
    return mapa


df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
m1 = df[df.stage.eq("primeira_fase")]

total_div = 0
for contest in sorted(m1.contest_id.unique()):
    pasta = ROOT / f"data/processed/text/{contest}"
    textos = list(pasta.rglob("prova_objetiva*.txt"))
    if not textos:
        continue
    mapa: dict[int, str] = {}
    for f in textos:
        try:
            mapa.update(mapa_secoes(f.read_text(encoding="utf-8", errors="replace")))
        except Exception as e:
            print(f"[!!] {f.name}: {e}")
    if not mapa:
        continue
    divs = []
    for qn, sec in sorted(mapa.items()):
        sub = m1[m1.contest_id.eq(contest) & m1.question_number.eq(float(qn))]
        if sub.empty:
            continue
        canon = sub.iloc[0]["discipline_canon"]
        if pd.isna(canon) or canon != sec:
            divs.append((qn, sec, canon))
    if divs:
        print(f"--- {contest}: {len(divs)} divergencias")
        for qn, sec, canon in divs:
            print(f"    q{qn}: prova={sec} | parquet={canon}")
        total_div += len(divs)

print(f"\nTOTAL divergencias: {total_div}")
