"""QA da Etapa 5: amostra de questoes para verificacao manual do gabarito.

Objetivo: depois de tudo extraido, sortear N questoes e, para cada uma, mostrar
o enunciado/alternativas e as respostas candidatas de CADA caderno do gabarito.
A pessoa resolve a questao e ve qual caderno bate — resolvendo a ambiguidade
multi-caderno (2003-2018, 2024) com evidencia humana.

Uso:
    python parser/qa.py --n 5                 # 5 questoes aleatorias (seed fixa)
    python parser/qa.py --n 5 --per-edition    # ate 5 por edicao
    python parser/qa.py --seed 7 --n 5
"""

from __future__ import annotations

import argparse
import ast
import random
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PROC = ROOT / "data" / "processed"
OUT_DIR = PROC / "qa_sample"


def load_answer_index() -> dict[str, list[dict]]:
    """contest_id -> lista de {source_file, caderno, answers(dict)}."""
    path = PROC / "answer_keys.parquet"
    out: dict[str, list[dict]] = {}
    if not path.exists():
        return out
    df = pd.read_parquet(path)
    for _, r in df.iterrows():
        sf = str(r["source_file"])
        contest = sf.split("/")[2] if sf.startswith("data/raw/") else ""
        try:
            answers = ast.literal_eval(str(r["answers"]))
        except Exception:
            answers = {}
        out.setdefault(contest, []).append(
            {"source_file": sf, "caderno": int(r.get("caderno", 0)), "answers": answers}
        )
    return out


def candidate_answers(q: pd.Series, index: dict[str, list[dict]]) -> dict:
    """Retorna {chave: {caderno: letra}} para a questao em cada arquivo de gabarito."""
    contest = q["contest_id"]
    qn = q["question_number"]
    item = q["item_number"]
    qtype = q["question_type"]

    def norm(x):
        if x is None or pd.isna(x):
            return None
        try:
            return int(float(x))
        except Exception:
            return None

    qn_i, item_i = norm(qn), norm(item)
    keys: list = []
    if qtype == "multiple_choice" and qn_i is not None:
        keys.append(qn_i)
    if item_i is not None:
        if qn_i is not None:
            keys.append((qn_i, item_i))
        keys.append(item_i)

    found: dict = {}
    for entry in index.get(contest, []):
        for k in keys:
            if k in entry["answers"]:
                found.setdefault(str(k), {})[entry["caderno"]] = entry["answers"][k]
    return found


def build_sample(
    n: int,
    per_edition: bool,
    seed: int,
    only_multi: bool = False,
    edition: str | None = None,
) -> pd.DataFrame:
    df = pd.read_parquet(PROC / "questions.parquet")
    index = load_answer_index()
    rng = random.Random(seed)

    # so questoes com enunciado minimo
    df = df[df["question_text"].fillna("").str.len() >= 40].copy()
    if edition:
        df = df[df["contest_id"] == edition].copy()

    # anexa candidatos e filtra para quem TEM gabarito candidato
    cands_series = df.apply(lambda q: candidate_answers(q, index), axis=1)
    df = df[cands_series.apply(bool)].copy()
    df["_cands"] = cands_series[df.index]
    if only_multi:
        df = df[df["_cands"].apply(lambda d: any(len(v) > 1 for v in d.values()))]
    df = df.copy()

    rows = []
    if per_edition:
        for _, g in df.groupby("contest_id"):
            picks = rng.sample(list(g.index), min(n, len(g)))
            rows.extend(picks)
    else:
        rows = rng.sample(list(df.index), min(n, len(df)))

    out = []
    for i in rows:
        q = df.loc[i]
        cands = df.loc[i, "_cands"]
        cadernos = sorted({c for d in cands.values() for c in d})

        def s(x, lim=600):
            if x is None or (isinstance(x, float) and pd.isna(x)):
                return ""
            return str(x)[:lim]

        out.append(
            {
                "question_id": q["question_id"],
                "contest_id": q["contest_id"],
                "discipline": s(q["discipline"], 80),
                "question_type": q["question_type"],
                "question_number": q["question_number"],
                "item_number": q["item_number"],
                "question_text": s(q["question_text"]),
                "item_text": s(q["item_text"]),
                "alternatives": s(q["alternatives"]),
                "answer_atual": s(q["answer"], 20),
                "candidatos": cands,
                "cadernos": cadernos,
                "source_file": q["source_file"],
                "resposta_humana": "",
                "caderno_que_bateu": "",
            }
        )
    return pd.DataFrame(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5, help="n de questoes (default 5)")
    ap.add_argument("--per-edition", action="store_true", help="ate n por edicao")
    ap.add_argument(
        "--only-multi",
        action="store_true",
        help="so questoes multi-caderno (para testar qual caderno bate)",
    )
    ap.add_argument("--edition", default=None, help="ex.: CACD_2019")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    sample = build_sample(
        args.n, args.per_edition, args.seed, args.only_multi, args.edition
    )
    if sample.empty:
        print("nenhuma questao com gabarito candidato encontrada")
        return
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    tag = "_multi" if args.only_multi else ""
    csv_path = OUT_DIR / f"sample_n{args.n}_seed{args.seed}{tag}.csv"
    md_path = OUT_DIR / f"sample_n{args.n}_seed{args.seed}{tag}.md"
    sample.to_csv(csv_path, index=False, encoding="utf-8")

    lines = [f"# Amostra de QA — {len(sample)} questoes (seed {args.seed})\n"]
    for j, r in sample.iterrows():
        lines.append(f"## {j + 1}. {r.contest_id} · {r.discipline} · q={r.question_number} item={r.item_number}")
        lines.append(f"- tipo: `{r.question_type}` · resposta atual: `{r.answer_atual}`")
        lines.append(f"- arquivo: `{r.source_file}`")
        lines.append(f"- enunciado: {r.question_text}")
        if r.item_text:
            lines.append(f"- item: {r.item_text}")
        if r.alternatives:
            lines.append(f"- alternativas: {r.alternatives}")
        lines.append(f"- **candidatos por caderno:** {r.candidatos}")
        lines.append("- resposta humana: ____  · caderno que bateu: ____\n")
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"amostra: {len(sample)} questoes")
    print(f"csv: {csv_path}")
    print(f"md : {md_path}\n")
    for j, r in sample.iterrows():
        print(f"[{j + 1}] {r.contest_id} q={r.question_number} item={r.item_number} "
              f"({r.question_type}) atual={r.answer_atual} candidatos={r.candidatos}")
        print(f"    {(r.question_text or '')[:140]}")


if __name__ == "__main__":
    main()
