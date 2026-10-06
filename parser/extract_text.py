"""
CACD Forecast AI - Etapa 4: extracao de texto dos PDFs.
Percorre data/raw/**/*.pdf, extrai texto com PyMuPDF e grava:
  data/processed/text/<contest_id>/<familia>/<arquivo>.txt
  data/processed/text_metrics.csv  (metricas de qualidade por arquivo)

Metricas: paginas, chars, questoes detectadas (regex QUESTAO N), taxa de
detecao proxy (chars/pagina), flag needs_ocr para PDFs quase vazios.

Uso:
    python parser/extract_text.py            # processa novos PDFs
    python parser/extract_text.py --sample 5 # so 5 arquivos (teste)
"""

import csv
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
TEXT = ROOT / "data" / "processed" / "text"
METRICS = ROOT / "data" / "processed" / "text_metrics.csv"

RE_QUESTION = re.compile(r"QUEST[ÃA]O\s+(\d+)", re.IGNORECASE)
MIN_CHARS_PER_PAGE = 120  # abaixo disso, provavel escaneado


def existing_processed():
    done = set()
    if METRICS.exists():
        with METRICS.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("ok") == "1":
                    done.add(r["pdf"])
    return done


def main():
    limit = None
    if "--sample" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--sample") + 1])

    TEXT.mkdir(parents=True, exist_ok=True)
    METRICS.parent.mkdir(parents=True, exist_ok=True)
    done = existing_processed()

    fields = [
        "pdf",
        "contest_id",
        "family",
        "pages",
        "chars",
        "chars_per_page",
        "questions_detected",
        "max_question",
        "needs_ocr",
        "ok",
        "error",
        "processed_at",
    ]
    new_manifest = not METRICS.exists()
    pdfs = sorted(RAW.glob("*/*.pdf")) + sorted(RAW.glob("*/*/*.pdf"))
    pdfs = sorted(set(pdfs))
    if limit:
        pdfs = pdfs[:limit]

    n_ok = n_ocr = n_fail = 0
    with METRICS.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if new_manifest:
            w.writeheader()
        for pdf in pdfs:
            key = str(pdf.relative_to(ROOT))
            if key in done:
                continue
            rel = pdf.relative_to(RAW)
            parts = rel.parts  # <contest_id>/<family>/<file>.pdf
            contest = parts[0]
            family = parts[1] if len(parts) > 2 else "root"
            out = TEXT / contest / family / (pdf.stem + ".txt")
            out.parent.mkdir(parents=True, exist_ok=True)

            row = {k: "" for k in fields}
            row.update(
                {
                    "pdf": key,
                    "contest_id": contest,
                    "family": family,
                    "processed_at": datetime.now(timezone.utc).isoformat(),
                }
            )
            try:
                doc = pymupdf.open(pdf)
                pages = doc.page_count
                text = "\n".join(p.get_text("text") for p in doc)
                doc.close()
                chars = len(text)
                cpp = chars / max(pages, 1)
                qs = RE_QUESTION.findall(text)
                row.update(
                    {
                        "pages": pages,
                        "chars": chars,
                        "chars_per_page": round(cpp, 1),
                        "questions_detected": len(set(qs)),
                        "max_question": max((int(q) for q in qs), default=0),
                        "needs_ocr": "1" if cpp < MIN_CHARS_PER_PAGE else "0",
                        "ok": "1",
                    }
                )
                out.write_text(text, encoding="utf-8")
                n_ok += 1
                if row["needs_ocr"] == "1":
                    n_ocr += 1
                    print(f"[OCR?] {key} ({cpp:.0f} chars/pag)")
            except Exception as e:
                row.update({"ok": "0", "error": str(e)[:150]})
                n_fail += 1
                print(f"[FAIL] {key}: {e}")
            w.writerow(row)
            f.flush()
            if n_ok % 25 == 0 and n_ok:
                print(f"  ... ok={n_ok} ocr={n_ocr} falhas={n_fail}")

    print(f"CONCLUIDO: ok={n_ok} needs_ocr={n_ocr} falhas={n_fail}")


if __name__ == "__main__":
    main()
