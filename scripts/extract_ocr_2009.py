"""Fase 4 (OCR) v2 — 3a/4a fase 2009: provas escritas por disciplina.

Estrategia: cada arquivo tem 4 questoes; cada questao ocupa 1 pagina de
enunciado + 2 de rascunho. OCR pagina a pagina (250 dpi, lang=por);
paginas com RASCUNHO no texto sao ignoradas; cada bloco QUESTAO N = 1 item.
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


def ocr_page(pg, dpi=250):
    pix = pg.get_pixmap(dpi=dpi)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return pytesseract.image_to_string(img, lang="por")


def clean(txt: str) -> str:
    t = re.sub(r"^\W*\s*(?:QUEST[ÃA]O\s+\d+)\s*[RN]?\s*", "", txt, flags=re.I)
    t = re.sub(r"\[?[LR]+QUEST[ÃA]O\s+\d+\s*[RN]*\s*\]?", "", t)
    t = re.sub(
        r"www\S+|UnB/CESPE.*|Instituto Rio Branco.*|Admiss[ãa]o.*|[–-]\s*\d+\s*[-–]",
        " ",
        t,
        flags=re.I,
    )
    return " ".join(t.replace("\n", " ").split()).strip()


SUBJ_PATTERNS = [
    ("HIST_DO_BRASIL|HISTORIA DO BRASIL", ("História do Brasil", 3)),
    ("ECONOMIA", ("Economia", 3)),
    ("GEOGRAFIA", ("Geografia", 3)),
    ("DIREITO_INTERNACIONAL_PUBLICO|DIREITO", ("Direito", 3)),
    ("INGLES", ("Língua Inglesa", 3)),
    ("POLIT_INTERNAC", ("Política Internacional", 3)),
    ("ESPANHOL", ("Espanhol e Francês", 4)),
    ("FRANCES", ("Espanhol e Francês", 4)),
    ("PORTUGUES", ("Língua Portuguesa", 2)),
]


def subject_of(pdf: Path):
    for pat, df in SUBJ_PATTERNS:
        if re.search(pat, pdf.stem, re.I):
            return df[0], df[1]
    return None, None


def main() -> None:
    folder = ROOT / "data/raw/CACD_2009/archive"
    recs = []
    for pdf in sorted(folder.glob("*.pdf")):
        if re.search(r"Gab|GAB|PARTE|TPS", pdf.stem, re.I):
            continue
        disc, fase = subject_of(pdf)
        if disc is None:
            print(f"[--] {pdf.name}: sem disciplina (ignorado)")
            continue
        with pymupdf.open(pdf) as doc:
            for pno, pg in enumerate(doc, 1):
                native = pg.get_text("text")
                # pula paginas de rascunho puro (so cabecalho/rodape, sem
                # conteudo de enunciado) — o cabecalho citando "RASCUNHO"
                # aparece em TODAS as paginas do caderno
                if "RASCUNHO" in native.upper() and "QUEST" not in native.upper():
                    continue
                if "QUEST" in native.upper() and len(native.strip()) >= 300:
                    txt = native
                else:
                    txt = ocr_page(pg)  # corpo fora da camada de texto
                if "RASCUNHO" in txt.upper():
                    continue
                qs = list(RE_Q.finditer(txt))
                if not qs:
                    continue
                for idx, m in enumerate(qs):
                    qn = int(m.group(1))
                    end = qs[idx + 1].start() if idx + 1 < len(qs) else len(txt)
                    body = clean(txt[m.end() : end])
                    if len(body) < 60:
                        continue
                    recs.append(
                        {
                            "contest_id": "CACD_2009",
                            "year": 2009,
                            "phase": fase,
                            "stage": {
                                2: "segunda_fase",
                                3: "terceira_fase",
                                4: "quarta_fase",
                            }[fase],
                            "discipline": disc,
                            "question_number": qn,
                            "item_number": None,
                            "question_type": "essay",
                            "question_text": body,
                            "item_text": None,
                            "alternatives": None,
                            "answer": None,
                            "page": pno,
                            "caderno": None,
                            "source_file": str(pdf.relative_to(ROOT)).replace(
                                "\\", "/"
                            ),
                            "source_url": None,
                            "confidence": 0.6,
                            "notes": "OCR (tesseract 5.4, por) — fonte sem camada de texto",
                        }
                    )
    out = ROOT / "data/raw/CACD_2009" / "discursivas_ocr_2009.jsonl"
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
    print(
        f"[ok] {out.name}: {len(recs)} registros | disciplinas: {sorted({r['discipline'] for r in recs})}"
    )


if __name__ == "__main__":
    main()
