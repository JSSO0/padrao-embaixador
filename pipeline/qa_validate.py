"""Validacao sistematica dos JSONL extraidos (2015-2018)."""

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECT = {
    2015: {1: range(1, 32), 2: range(32, 74)},
    2016: {1: range(1, 32), 2: range(32, 74)},
    2017: {1: range(1, 35), 2: range(35, 74)},
    2018: {1: range(1, 35), 2: range(35, 74)},
    2019: {1: range(1, 35), 2: range(35, 74)},
    "2020_2021": {1: range(1, 35), 2: range(35, 74)},
    2022: {1: range(1, 35), 2: range(35, 74)},
    2023: {1: range(1, 36), 2: range(36, 74)},
}

for year, parts in EXPECT.items():
    for part, rng in parts.items():
        f = (
            ROOT
            / f"data/raw/CACD_{year}/cursocacd/cacd_{year}_primeira_fase_prova_objetiva_{part}.jsonl"
        )
        recs = [json.loads(l) for l in f.open(encoding="utf-8")]
        by_q: dict[int, list] = {}
        for r in recs:
            by_q.setdefault(r["question_number"], []).append(r)
        nums = sorted(by_q)
        missing = [n for n in rng if n not in by_q]
        extra = [n for n in nums if n not in rng]
        bad_items = {
            n: len(v)
            for n, v in by_q.items()
            if len([x for x in v if x["item_number"] is not None]) != 4
        }
        empty_item = [
            r["question_number"]
            for r in recs
            if r["item_number"] is not None and not (r["item_text"] or "").strip()
        ]
        no_julgue = [
            n
            for n, v in by_q.items()
            if not re.search(
                r"julg|mark right|decide whether",
                (v[0]["question_text"] or ""),
                re.I,
            )
        ]
        short_qt = [n for n, v in by_q.items() if len(v[0]["question_text"] or "") < 40]
        print(
            f"{year} p{part}: questoes={len(nums)} faltando={missing} extra={extra} "
            f"itens!=4={bad_items} item_vazio={sorted(set(empty_item))} "
            f"sem_julgue={sorted(set(no_julgue))} qt_curta={sorted(set(short_qt))}"
        )
