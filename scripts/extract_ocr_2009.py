"""Fase 4 (OCR) — 3a/4a fase 2009: provas escritas por disciplina (corpo fora
da camada de texto). Renderiza a 250 dpi, OCR lang=por, blocos QUESTAO N
ate RASCUNHO/proxima questao.
"""

import io
import json
import os
import re
from pathlib import Path

import pymupdf

os.environ["TESSDATA_PREFIX"] = str(Path(os.environ["LOCALAPPDATA"]) / "tessdata")
os.environ["PATH"] += r";C:\Program Files\Tesseract-OCR"
import pytesseract  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SUBJ = {
    "HIST_DO_BRASIL": ("História do Brasil", 3),
    "ECONOMIA": ("Economia", 3),
    "GEOGRAFIA": ("Geografia", 3),
    "DIREITO": ("Direito", 3),
    "INGLES": ("Língua Inglesa", 3),
    "ESPANHOL": ("Espanhol e Francês", 4),
    "FRANCES": ("Espanhol e Francês", 4),
    "PORTUGUES": ("Língua Portuguesa", 2),
}
RE_Q = re.compile(r"QUEST[ÃA]O\s+(\d{1,2})", re.I)
RE_RASC = re.compile(r"RASCUNHO", re.I)


def ocr_page(pg, dpi=250):
    pix = pg.get_pixmap(dpi=dpi)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return pytesseract.image_to_string(img, lang="por")


def main() -> None:
    folder = ROOT / "data/raw/CACD_2009/archive"
    recs = []
    for stem, (disc, fase) in SUBJ.items():
        pdf = folder / f"IRBR_{stem}_3a_fase_1a_etapa.pdf"
        if not pdf.exists():
            pdf = folder / f"IRBR_{stem}.pdf"
        if not pdf.exists():
            continue
        with pymupdf.open(pdf) as doc:
            pages = []
            for pno, pg in enumerate(doc, 1):
                txt = pg.get_text("text")
                if len(txt.strip()) < 900:  # pagina quase vazia no texto nativo
                    txt = ocr_page(pg)
                pages.append((pno, txt))
        # blocos QUESTAO N ate RASCUNHO/proxima QUESTAO
        full_lines = []
        for pno, txt in pages:
            for ln in txt.split("\n"):
                if ln.strip():
                    full.append if False else None
            for ln in re.split(r"\n", "\n".join(p[1] for p in pages)):
                pass
        # reconstroi full na ordem das paginas
        full = "\n".join(t for _, t in pages)
        qs = sorted(
            (m.start(), int(m.group(1)))
            for m in re.finditer(r"QUEST[ÃA]O\s+(\d{1,2})", full)
        )
        for idx, (pos, qn) in enumerate(qs):
            ends = [p for p, n in qs if p > pos and n == qn + 1]
            end = ends[0] if ends else len(full)
            body = re.sub(
                r"\[?\s*[LC]+QUEST[ÃA]O\s+\d+\s*[RN]*\s*\]?", "", full[pos:end]
            )
            body = " ".join(body.replace("\n", " ").split())
            if len(body) < 80:
                continue
            recs.append(
                {
                    "contest_id": "CACD_2009",
                    "year": 2009,
                    "phase": fase,
                    "stage": {2: "segunda_fase", 3: "terceira_fase", 4: "quarta_fase"}[
                        fase
                    ],
                    "discipline": disc,
                    "question_number": qn,
                    "item_number": None,
                    "question_type": "essay",
                    "question_text": body,
                    "item_text": None,
                    "alternatives": None,
                    "answer": None,
                    "page": None,
                    "caderno": None,
                    "source_file": str(pdf.relative_to(ROOT)).replace("\\", "/"),
                    "source_url": None,
                    "confidence": 0.6,
                    "notes": "OCR (tesseract 5.4, por) — fonte sem camada de texto",
                }
            )
    out = ROOT / "data/raw/CACD_2009" / "discursivas_ocr_2009.jsonl"
    # dedup: uma questao por (disciplina, numero)
    vistos, unicos = set(), []
    for r in recs:
        k = (r["discipline"], r["question_number"])
        if k not in vistos:
            vistos.add(k)
            unicos.append(r)
    recs = unicos
    with out.open("w", encoding="utf-8") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[ok] {out.name}: {len(recs)} registros")


if __name__ == "__main__":
    main()
