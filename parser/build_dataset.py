"""Orquestrador da Etapa 5: corpus -> questions.parquet + extraction_report.

Uso:
    python parser/build_dataset.py                     # processa tudo
    python parser/build_dataset.py --edition CACD_2026 # so uma edicao
    python parser/build_dataset.py --sample 3          # so 3 documentos (teste)
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from parser.answer_merger import extract_answer_key, merge_answers  # noqa: E402
from parser.document_loader import (  # noqa: E402
    load_catalog_index,
    load_manifest,
    load_pdf,
    looks_like_exam,
    source_type_for,
)
from parser.models import SOURCE_PRIORITY  # noqa: E402
from parser.parsers.base import get_parser  # noqa: E402

RAW = ROOT / "data" / "raw"
OUT_Q = ROOT / "data" / "processed" / "questions.parquet"
OUT_REPORT = ROOT / "data" / "processed" / "extraction_report.csv"
OUT_KEYS = ROOT / "data" / "processed" / "answer_keys.parquet"

SKIP_DOCTYPES = {
    "edital",
    "edital_retificacao",
    "resultado",
    "gabarito_justificativa",
    "padrao_resposta",
    "guia_estudos",
    "edital_index",
    "arquivo_provas_antigas",
    "pagina_concurso",
    "provas_pacote",
    "pagina_indice",
    "pagina_prova",
}
PROVA_DOCTYPES = {"prova", "prova_objetiva", "prova_discursiva", "provas"}
NAME_SKIP = ("edital", "resultado", "demanda", "comunicado", "isen", "padrao", "guia")


def classify(
    pdf: Path, catalog: dict[str, dict], manifest: dict[str, dict]
) -> tuple[str, str]:
    """Retorna (doc_role, source_type) via manifest -> url -> catalogo."""
    rel_path = str(pdf.relative_to(ROOT)).replace("\\", "/")
    murl = ""
    for r in manifest.values():
        if r.get("file_path") == rel_path:
            murl = r.get("url", "")
            break
    row = catalog.get(murl, {})
    doc_type = row.get("doc_type", "")
    stype = source_type_for(pdf, manifest)
    stem = pdf.stem.lower()
    if doc_type in SKIP_DOCTYPES:
        return "outro", stype
    if "gabarito" in stem:
        return "gabarito", stype
    if doc_type in PROVA_DOCTYPES:
        return "prova", stype
    if any(w in stem for w in NAME_SKIP):
        return "outro", stype
    return "prova", stype


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition")
    ap.add_argument("--sample", type=int, default=0)
    args = ap.parse_args()

    manifest = load_manifest()
    catalog = load_catalog_index()
    pdfs = sorted(set(RAW.glob("*/*/*.pdf")) | set(RAW.glob("*/*.pdf")))
    if args.edition:
        pdfs = [p for p in pdfs if p.parent.parent.name == args.edition]
    if args.sample:
        pdfs = pdfs[: args.sample]
    print(f"documentos: {len(pdfs)}")

    exams: list = []
    answer_keys: list[tuple[str, dict[int, str]]] = []
    report_rows: list[dict] = []

    for pdf in pdfs:
        rel = str(pdf.relative_to(ROOT)).replace("\\", "/")
        contest = pdf.relative_to(RAW).parts[0]
        role, stype = classify(pdf, catalog, manifest)
        row = {
            "contest_id": contest,
            "source_file": rel,
            "family": pdf.parent.name,
            "doc_role": role,
            "parser": "",
            "questions_found": 0,
            "status": "",
            "issues": "",
        }
        try:
            if role == "outro":
                row.update(
                    {"status": "skipped", "reason": "edital/resultado/padrao/guia"}
                )
            elif role == "gabarito":
                doc = load_pdf(pdf, ROOT)
                key, warns = extract_answer_key(doc)
                answer_keys.append((rel, key))
                row.update(
                    {
                        "status": "gabarito",
                        "questions_found": len(key),
                        "issues": "; ".join(warns)[:200],
                    }
                )
            else:
                doc = load_pdf(pdf, ROOT)
                if not looks_like_exam(doc):
                    row.update(
                        {
                            "status": "skip_nao_exame",
                            "reason": "nao parece caderno de prova",
                        }
                    )
                else:
                    parser = get_parser(doc)
                    exam = parser.parse(doc)
                    for q in exam.questions:
                        q.source_type = getattr(q, "source_type", stype) or stype
                    exams.append(exam)
                    row.update(
                        {
                            "parser": type(parser).__name__,
                            "questions_found": len(exam.questions),
                            "status": "ok",
                            "issues": "; ".join(exam.warnings)[:200],
                        }
                    )
        except Exception as e:
            row.update({"status": "erro", "issues": str(e)[:150]})
        report_rows.append(row)
        print(f"[{row['status']}] {rel} -> {row.get('questions_found', 0)}")

    # gabaritos por edicao (definitivo por ultimo na lista -> vence no merge)
    all_questions: list = []
    for exam in exams:
        prefix = f"data/raw/{exam.contest_id}".replace("\\", "/")
        keys = [(name, key) for name, key in answer_keys if name.startswith(prefix)]
        # ordenação inteligente: definitivo primeiro no final? queremos definitivo vencer -> vai pro fim
        # calcular range das questões do exame
        nums_exam = []
        for q in exam.questions:
            num = getattr(q, "question_number", None) or getattr(q, "item_number", None)
            if num is not None:
                try:
                    num = int(float(num))
                    nums_exam.append(num)
                except Exception:
                    pass
        min_n = min(nums_exam) if nums_exam else 0
        max_n = max(nums_exam) if nums_exam else 9999
        keys_sorted = sorted(
            keys,
            key=lambda kv: (
                "definitivo" not in kv[0].lower(),  # definitivo fica no fim
                # penalizar gabaritos com range muito fora das questões
                -(
                    1
                    if nums_exam
                    and min(kv[1].keys()) >= min_n - 2
                    and max(kv[1].keys()) <= max_n + 2
                    else 0
                ),
                abs(len(kv[1]) - len(nums_exam)) if nums_exam else 0,
                kv[0],
            ),
        )
        warns = merge_answers(exam.questions, keys_sorted)
        exam.warnings.extend(warns)
        all_questions.extend(exam.questions)

    # dedup por (contest, stage, disciplina, numero, item, tipo): melhor fonte vence
    seen: dict[tuple, object] = {}
    dup_count = 0
    for q in all_questions:
        k = (
            q.contest_id,
            q.stage,
            q.discipline,
            getattr(q, "question_number", None),
            getattr(q, "item_number", None),
            q.question_type,
        )
        if k in seen:
            if SOURCE_PRIORITY.get(
                getattr(q, "source_type", "unknown"), 9
            ) < SOURCE_PRIORITY.get(getattr(seen[k], "source_type", "unknown"), 9):
                seen[k] = q
            dup_count += 1
            continue
        seen[k] = q
    final = list(seen.values())

    recs = [
        {
            "question_id": q.question_id,
            "parent_question_id": q.parent_question_id,
            "contest_id": q.contest_id,
            "year": q.year,
            "phase": q.phase,
            "stage": q.stage,
            "discipline": q.discipline,
            "question_number": getattr(q, "question_number", None),
            "item_number": getattr(q, "item_number", None),
            "question_type": q.question_type,
            "question_text": q.question_text,
            "item_text": getattr(q, "item_text", None),
            "alternatives": " | ".join(f"{a.letter}) {a.text}" for a in q.alternatives)
            if q.alternatives
            else None,
            "answer": q.answer,
            "source_type": getattr(q, "source_type", "unknown"),
            "source_file": q.source_file,
            "extraction_method": q.extraction_method,
            "warnings": ";".join(q.warnings) if q.warnings else None,
        }
        for q in final
    ]

    OUT_Q.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(recs)
    df.to_parquet(OUT_Q, index=False)
    pd.DataFrame(report_rows).to_csv(OUT_REPORT, index=False, encoding="utf-8")

    # salvar answer_keys
    try:
        OUT_KEYS.parent.mkdir(parents=True, exist_ok=True)
        keys_df = pd.DataFrame(
            [{"source_file": name, "answers": key} for name, key in answer_keys]
        )
        # serializar dicts para formato compatível com parquet
        if not keys_df.empty:
            keys_df = keys_df.assign(answers=lambda x: x["answers"].apply(str))
        keys_df.to_parquet(OUT_KEYS, index=False)
    except Exception as e:
        print("warn: não salvou answer_keys:", e)

    print(
        f"== questoes/itens: {len(df)} | docs prova: {len(exams)} | gabaritos: {len(answer_keys)}"
    )
    if len(df):
        print(df.groupby("contest_id").size().to_string())
        print("por tipo:", df.question_type.value_counts().to_dict())
        print(f"com gabarito: {df['answer'].notna().mean():.1%}")


if __name__ == "__main__":
    main()
