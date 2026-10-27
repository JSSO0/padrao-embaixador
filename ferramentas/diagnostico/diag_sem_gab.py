"""Lista todas as questoes objetivas sem gabarito, agrupadas por causa."""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "data/processed/questions.parquet")
g = json.load(open(ROOT / "data/processed/gabaritos.json", encoding="utf-8"))

m = df[df.stage.eq("primeira_fase")]
sem = m[~(m.answer.notna() & m.answer.astype(str).str.strip().ne(""))]

print(f"Total sem gabarito: {len(sem)} de {len(m)}")
print()

for contest, grp in sem.groupby("contest_id"):
    year = contest.replace("CACD_", "")
    ano_gab = "2003" if contest == "CACD_2003" else year
    cache = g.get(ano_gab, {})

    print(f"--- {contest} ({len(grp)} itens) ---")
    for _, r in grp.sort_values("question_number").iterrows():
        qn = int(float(r["question_number"]))
        itn = r["item_number"]
        itn_v = int(float(itn)) if pd.notna(itn) else None
        # tenta encontrar a chave no gabarito
        keys_to_try = []
        if itn_v is not None:
            keys_to_try.append(f"{qn}:{itn_v}")
            if contest == "CACD_2004":
                keys_to_try.append(f"{(qn - 1) * 5 + itn_v}:1")
        if pd.isna(itn):
            keys_to_try.append(f"{qn}:0")
            keys_to_try.append(f"{qn}:1")
            keys_to_try.append(f"{(qn - 1) * 5 + 1}:1")
        found = [k for k in keys_to_try if k in cache]
        if found:
            print(
                f"  qn={qn} itn={itn} | CHAVE EXISTE: {found[0]} = {cache[found[0]]!r} | {str(r.question_text)[:40]!r}"
            )
        else:
            # mostra quais chaves existem para essa questao
            existentes = [k for k in cache if k.startswith(f"{qn}:")]
            if existentes:
                print(
                    f"  qn={qn} itn={itn} | chaves no cache: {existentes[:5]} | {str(r.question_text)[:40]!r}"
                )
            else:
                print(
                    f"  qn={qn} itn={itn} | NADA no cache | {str(r.question_text)[:50]!r}"
                )
    print()
