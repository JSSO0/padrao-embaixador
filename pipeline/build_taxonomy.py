# -*- coding: utf-8 -*-
"""Aplica a taxonomia tematica de data/metadata/taxonomia.yaml aos itens da
1a fase (M2.1/M2.3).

Metodo (regras-fixas-a-priori): a classificacao de um item usa APENAS o
texto do proprio item (question_text + item_text) e as palavras-chave deste
arquivo. Nao ha ajuste por corpus, similaridade global ou uso de outros
itens — sem vazamento temporal. Sem match de keyword, aplica o fallback da
disciplina (tema mais amplo), nunca "geral".

Este script substitui o antigo trio build_taxonomy.py ->
refine_taxonomy.py -> refine_taxonomy_tfidf.py (o ultimo usava TF-IDF sobre
o corpus inteiro, um vazamento temporal).

Uso: python pipeline/build_taxonomy.py [--dry-run]
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "data/metadata/taxonomia.yaml"
PATH = ROOT / "data/processed/questions.parquet"


def carregar_taxonomia() -> dict:
    doc = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))["taxonomia"]
    return doc


def classify(texto: str, disc: str, tax: dict) -> tuple[str, bool]:
    """(tema, houve_keyword) — contagem de keywords por tema da disciplina;
    sem match, fallback da disciplina. Depende apenas de (texto, disc, YAML)."""
    temas = tax["disciplinas"].get(disc, {})
    lower = texto.lower()
    best, best_score = None, 0
    for tema, info in temas.items():
        score = sum(1 for kw in info["keywords"] if kw.lower() in lower)
        if score > best_score:
            best, best_score = tema, score
    if best is None:
        return tax["fallback"][disc], False
    return best, True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    tax = carregar_taxonomia()
    df = pd.read_parquet(PATH)
    n_sem_disc = int((df.stage.eq("primeira_fase") & df.discipline_canon.isna()).sum())

    df["topic"] = None
    n_fallback = 0
    for idx in df.index[df.stage.eq("primeira_fase")]:
        disc = df.at[idx, "discipline_canon"]
        if pd.isna(disc) or disc not in tax["disciplinas"]:
            continue
        texto = (
            str(df.at[idx, "question_text"]) + " " + str(df.at[idx, "item_text"] or "")
        )
        tema, matched = classify(texto, disc, tax)
        n_fallback += int(not matched)
        df.at[idx, "topic"] = tema

    if args.dry_run:
        print("dry-run: nada escrito")
        return

    df.to_parquet(PATH, index=False)
    print(f"=== Taxonomia v{tax['version']} aplicada (metodo: {tax['metodo']}) ===")
    sem = df[df.stage.eq("primeira_fase") & df.topic.isna()]
    print(f"itens sem tema: {int(len(sem))} | por fallback: {n_fallback}")
    st = df[df.stage.eq("primeira_fase")].topic.fillna("(sem tema)").value_counts()
    print(st.to_string())


if __name__ == "__main__":
    main()
