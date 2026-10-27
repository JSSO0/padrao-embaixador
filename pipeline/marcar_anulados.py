"""Marca itens anulados da 1a fase (M1.5): notes = "anulado" em todo item
cujo gabarito oficial (data/processed/gabaritos.json) tem X/#/☼.

Aceite (M1.5): 100% dos itens anulados com o motivo em `notes`; o QA
(ferramentas/extracoes_pontuais/extract_faltantes.py) exibe
"ANULADO pela banca" quando notes contem "anulado".

Itens sem resposta SEM chave no gabarito ficam sem note aqui — o motivo deles
vem do OCR do M1.6.

Uso: python pipeline/marcar_anulados.py [--dry-run]
"""

import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "processed" / "questions.parquet"
CACHE = ROOT / "data" / "processed" / "gabaritos.json"


def num(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


df = pd.read_parquet(PATH)
g = json.loads(CACHE.read_text(encoding="utf-8"))

m = df.stage.eq("primeira_fase") & df.extraction_method.isin(["manual", "rules"])

marcados = ja_ok = sem_gabarito = com_resposta_conflito = 0
for idx in df[m].index:
    row = df.loc[idx]
    contest = str(row["contest_id"])
    y = "2003" if contest == "CACD_2003" else str(int(row["year"]))
    qn = num(row["question_number"])
    itn = num(row["item_number"])
    yg = g.get(y) or {}
    letter = None
    if qn is not None:
        if itn is not None:
            letter = yg.get(f"{qn}:{itn}")
        else:
            letter = yg.get(f"{qn}:0") or yg.get(f"{qn}:1")
    if letter is None:
        sem_gabarito += 1
        continue
    if str(letter).upper() not in ("X", "#", "☼"):
        continue
    has_ans = pd.notna(row["answer"]) and bool(str(row["answer"]).strip())
    if has_ans:
        # gabarito oficial diz anulada mas a linha tem resposta: corrige
        com_resposta_conflito += 1
        df.at[idx, "answer"] = None
    note = row.get("notes")
    if pd.isna(note) or not str(note).strip():
        df.at[idx, "notes"] = "anulado"
        marcados += 1
    elif "anulado" in str(note).lower():
        ja_ok += 1

print(f"anulados marcados agora: {marcados}")
print(f"ja marcados antes: {ja_ok}")
print(f"anulados com resposta (corrigidos para null): {com_resposta_conflito}")
print(f"sem resposta e sem chave no gabarito (fica para o M1.6/OCR): {sem_gabarito}")

ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()
if args.dry_run:
    print("dry-run: nada escrito")
    raise SystemExit(0)

df.to_parquet(PATH, index=False)
print(f"parquet salvo: {PATH}")
