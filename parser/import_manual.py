"""Importa transcricoes manuais (JSON/JSONL) para o dataset de questoes.

A IA externa (ou revisao humana) grava arquivos .json/.jsonl/.txt com objetos
JSON (um por questao/item) em data/raw/<contest_id>/... O importador:
  - le todos os objetos (JSONL ou JSON concatenado, tolerante a BOM/espacos)
  - normaliza campos (question_type, discipline, contest_id)
  - resolve source_file (basename -> caminho relativo real sob data/raw)
  - valida com Pydantic e calcula question_id deterministico
  - funde em data/processed/questions.parquet (manual VENCE o rules)

Uso:
    python parser/import_manual.py --dry-run   # so relatorio, nao escreve
    python parser/import_manual.py             # importa e funde
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from parser.document_loader import source_type_for  # noqa: E402
from parser.models import Question, question_id  # noqa: E402
from parser.parsers.base import normalize_disc  # noqa: E402

RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
OUT_Q = PROC / "questions.parquet"
OUT_REPORT = PROC / "manual_import_report.csv"

QTYPE_MAP = {
    "multipla_escolha": "multiple_choice",
    "multipla escolha": "multiple_choice",
    "multiple_choice": "multiple_choice",
    "multiple choice": "multiple_choice",
    "certo_errado": "certo_errado",
    "certo/errado": "certo_errado",
    "certo ou errado": "certo_errado",
    "discursiva": "essay",
    "essay": "essay",
}


def iter_objects(text: str):
    """Le objetos JSON concatenados (JSONL ou pretty-printed)."""
    dec = json.JSONDecoder()
    i = 0
    n = len(text)
    while i < n:
        while i < n and text[i] in " \r\n\t":
            i += 1
        if i >= n:
            break
        obj, j = dec.raw_decode(text, i)
        yield obj
        i = j


_RE_STR_LINE = re.compile(r'^(\s*"[^"]+"\s*:\s*")(.*)("[,]?\s*)$')


def repair_unescaped_quotes(text: str) -> str:
    """Best-effort: escapa aspas nao escapadas dentro de valores de string de
    uma unica linha (erro comum de saida de IA). Nao mexe em linhas que ja sao
    JSON valido (sem aspas internas)."""
    out = []
    for line in text.split("\n"):
        m = _RE_STR_LINE.match(line)
        if m:
            inner = re.sub(r'(?<!\\)"', r'\\"', m.group(2))
            line = m.group(1) + inner + m.group(3)
        out.append(line)
    return "\n".join(out)


def pdf_index() -> dict[str, str]:
    """basename do PDF -> caminho relativo (para resolver source_file)."""
    out: dict[str, str] = {}
    for p in RAW.glob("*/*/*.pdf"):
        out.setdefault(p.name, str(p.relative_to(ROOT)).replace("\\", "/"))
    for p in RAW.glob("*/*.pdf"):
        out.setdefault(p.name, str(p.relative_to(ROOT)).replace("\\", "/"))
    return out


def find_manual_files() -> list[Path]:
    files: list[Path] = []
    for p in RAW.glob("**/*"):
        if p.suffix.lower() not in (".json", ".jsonl", ".txt"):
            continue
        try:
            head = p.read_text(encoding="utf-8", errors="ignore").lstrip("\ufeff \r\n\t")[:1]
        except Exception:
            continue
        if head == "{":
            files.append(p)
    return sorted(files)


def norm_type(v) -> str | None:
    if not v:
        return None
    return QTYPE_MAP.get(str(v).strip().lower())


def build_question(obj: dict, pdfs: dict[str, str], contest_dir: str) -> tuple[Question | None, str]:
    sf = str(obj.get("source_file") or "").strip()
    full = ""
    if sf:
        cand = pdfs.get(Path(sf).name)
        if cand:
            full = cand
    if not full:
        # tenta achar por basename em qualquer lugar
        cand = pdfs.get(Path(sf).name) if sf else None
        full = cand or sf
    # contest_id: do caminho do pdf > diretorio do arquivo > campo
    contest = ""
    if full.startswith("data/raw/"):
        contest = full.split("/")[2]
    contest = contest or contest_dir or (obj.get("contest_id") or "")
    if not contest:
        return None, "sem contest_id resolvivel"

    qtype = norm_type(obj.get("question_type"))
    if qtype is None:
        return None, f"question_type invalido: {obj.get('question_type')!r}"

    year = obj.get("year")
    try:
        year = int(year)
    except Exception:
        year = int(contest.replace("CACD_", "").split("_")[0]) if contest else 0

    disc = obj.get("discipline")
    disc = normalize_disc(disc) if disc else None

    stage = obj.get("stage") or ("primeira_fase" if obj.get("phase") == 1 else "segunda_fase")
    phase = obj.get("phase")
    try:
        phase = int(phase)
    except Exception:
        phase = 1

    stype = source_type_for(Path(full), {}) if full else "unknown"

    alts = []
    for a in obj.get("alternatives") or []:
        if isinstance(a, dict) and a.get("letter") is not None:
            alts.append({"letter": str(a["letter"]), "text": str(a.get("text", ""))})

    qn = obj.get("question_number")
    itn = obj.get("item_number")
    try:
        qn = int(qn) if qn is not None else None
    except Exception:
        qn = None
    try:
        itn = int(itn) if itn is not None else None
    except Exception:
        itn = None

    try:
        q = Question(
            question_id=question_id(contest, stage, disc, qn, itn),
            contest_id=contest,
            year=year,
            phase=phase,
            stage=stage,
            discipline=disc,
            question_number=qn,
            item_number=itn,
            item_text=obj.get("item_text"),
            question_type=qtype,
            question_text=str(obj.get("question_text") or ""),
            alternatives=alts,
            answer=obj.get("answer"),
            source_type=stype,
            source_file=full,
            page=obj.get("page"),
            extraction_method="manual",
        )
    except Exception as e:
        return None, f"validacao: {e}"
    return q, ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pdfs = pdf_index()
    files = find_manual_files()
    print(f"arquivos manuais encontrados: {len(files)}")

    manual: list[Question] = []
    report = []
    for f in files:
        contest_dir = f.relative_to(RAW).parts[0] if f.relative_to(RAW).parts else ""
        text = f.read_text(encoding="utf-8", errors="replace")
        objs: list = []
        note = ""
        try:
            objs = list(iter_objects(text))
        except json.JSONDecodeError as e:
            try:
                objs = list(iter_objects(repair_unescaped_quotes(text)))
                note = f"reparado automaticamente ({e})"
            except json.JSONDecodeError as e2:
                report.append(
                    {"file": str(f.relative_to(ROOT)), "ok": 0, "erros": 0, "status": "JSON invalido", "detalhe": f"JSON invalido: {e2}"}
                )
                print(f"[ERRO] {f.name}: JSON invalido: {e2}")
                continue
        ok = 0
        errs = 0
        last_err = ""
        for obj in objs:
            q, err = build_question(obj, pdfs, contest_dir)
            if q is None:
                errs += 1
                last_err = err
            else:
                manual.append(q)
                ok += 1
        report.append(
            {"file": str(f.relative_to(ROOT)), "ok": ok, "erros": errs, "status": "ok", "detalhe": note or last_err}
        )
        print(f"[ok] {f.name}: {ok} questoes ({errs} descartadas){' [' + note + ']' if note else ''}")

    # dedup por question_id (ultimo vence)
    by_id: dict[str, Question] = {}
    for q in manual:
        by_id[q.question_id] = q
    manual = list(by_id.values())
    print(f"total manual (dedup): {len(manual)}")

    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(report).to_csv(OUT_REPORT, index=False, encoding="utf-8")

    if args.dry_run or not manual:
        print("dry-run: nada escrito")
        return

    # funde no parquet: manual substitui rules do MESMO documento (source_file)
    old = pd.read_parquet(OUT_Q) if OUT_Q.exists() else pd.DataFrame()
    manual_ids = set(by_id.keys())
    manual_files = {q.source_file for q in manual}
    if len(old):
        old = old[~old["question_id"].isin(manual_ids)]
        if manual_files:
            old = old[~old["source_file"].isin(manual_files)]
    recs = []
    for q in manual:
        recs.append(
            {
                "question_id": q.question_id,
                "parent_question_id": q.parent_question_id,
                "contest_id": q.contest_id,
                "year": q.year,
                "phase": q.phase,
                "stage": q.stage,
                "discipline": q.discipline,
                "question_number": q.question_number,
                "item_number": q.item_number,
                "question_type": q.question_type,
                "question_text": q.question_text,
                "item_text": q.item_text,
                "alternatives": " | ".join(f"{a.letter}) {a.text}" for a in q.alternatives) or None,
                "answer": q.answer,
                "source_type": q.source_type,
                "source_file": q.source_file,
                "extraction_method": q.extraction_method,
                "warnings": ";".join(q.warnings) if q.warnings else None,
            }
        )
    df = pd.concat([old, pd.DataFrame(recs)], ignore_index=True) if len(old) else pd.DataFrame(recs)
    df.to_parquet(OUT_Q, index=False)
    print(f"questions.parquet: {len(old)} rules + {len(recs)} manual = {len(df)}")


if __name__ == "__main__":
    main()
