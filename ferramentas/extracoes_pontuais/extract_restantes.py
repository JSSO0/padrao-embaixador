"""Extrai provas escritas 2003-2012 que faltam: nome flexivel + OCR quando
texto nativo tem poucos caracteres.

Cobre: 2003 (2a fase Port/Ing), 2004 (disc Port/Ing), 2005 (TPS prova),
2006 (TPS manha/tarde), 2007 (IRBr_001_1-4), 2008/2009 (escrita),
2010 (per-disciplina), 2011-2012 (concurso completo).
"""

import glob
import json
import io
import os
import re
from pathlib import Path

import pymupdf

os.environ["TESSDATA_PREFIX"] = str(Path(os.environ["LOCALAPPDATA"]) / "tessdata")
os.environ["PATH"] += r";C:\Program Files\Tesseract-OCR"
import pytesseract  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RE_Q = re.compile(r"QUEST[ÃA]O\s+(\d{1,2})", re.I)
RE_ESSAY = re.compile(
    r"Extens[ãa]o m[áa]xima|valor da quest[ãa]o|Comente|Escreva|Elabore", re.I
)
RE_MC = re.compile(r"Assinale a op[çc][ãa]o", re.I)


def norm(s: str) -> str:
    return " ".join(s.replace("\n", " ").split()).strip()


def ocr_page(pg, dpi=250):
    pix = pg.get_pixmap(dpi=250)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return pytesseract.image_to_string(img, lang="por")


def subject_from_content(t: str, stem: str):
    """Tenta descobrir a disciplina pelo conteudo."""
    m = re.search(r"PROVA ESCRITA DE ([A-ZÀ-Úa-zà-ú ]{3,80})", t)
    if m:
        s = m.group(1).strip().upper()
        for k, v in {
            "PORTUG": "Língua Portuguesa",
            "INGL": "Língua Inglesa",
            "ESPANH": "Espanhol e Francês",
            "FRANC": "Espanhol e Francês",
            "ALEM": "Alemão",
            "HIST": "História do Brasil",
            "GEOGR": "Geografia",
            "POLIT": "Política Internacional",
            "ECON": "Economia",
            "DIREITO": "Direito",
            "INTERNACIONAL PÚBLICO": "Direito",
        }.items():
            if k := s.startswith(pat):
                if pat := next((k2 for k2 in [s] if True), ""):
                    pass
    # fallback: nome do arquivo
    u = stem.upper()
    for pat, disc in [
        ("PORT_ESCR|PROVA_DISC_PORT|PORTUGUES", "Língua Portuguesa"),
        ("INGLES|ING_ESCR", "Língua Inglesa"),
        ("ESPANHOL", "Espanhol e Francês"),
        ("FRANCES", "Espanhol e Francês"),
        ("ALEMAO", "Alemão"),
        ("HISTORIA", "História do Brasil"),
        ("GEOGRAFIA", "Geografia"),
        ("DIREITO", "Direito"),
        ("ECONOMIA", "Economia"),
        ("POLITICA INTERNACIONAL", "Política Internacional"),
    ]:
        if re.search(pat, u):
            return disc
    return None


def fase_from_name(stem: str):
    u = stem.upper()
    if re.search(r"SEGUNDA|2A", u):
        return 2, "segunda_fase"
    if re.search(r"3A|TERCEIRA", u):
        return 3, "terceira_fase"
    if re.search(r"4A|QUARTA", u):
        return 4, "quarta_fase"
    return 2, "segunda_fase"


def main() -> None:
    total = 0
    for y in range(2003, 2013):
        folder = ROOT / "data/raw" / f"CACD_{y}" / "archive"
        if not folder.exists():
            continue
        recs = []
        for pdf in sorted(folder.glob("*.pdf")):
            if re.search(r"Gab|gabarito|GAB", pdf.stem, re.I):
                continue
            # pula os que ja foram processados
            skip_names = [
                "questoes_faltantes_2010.jsonl",
            ]
            # testa se ja existe saida para este PDF
            existing = list(folder.glob(f"discursivas_ocr*{pdf.stem[:20]}*"))
            if existing:
                continue
            # processa
            with pymupdf.open(pdf) as doc:
                native = "".join(pg.get_text("text") for pg in doc)
                npages = len(doc)
            if len(native) < 4000:
                # OCR todas as paginas
                with pymupdf.open(pdf) as doc:
                    native = "\n".join(
                        pytesseract.image_to_string(
                            Image.open(
                                io.BytesIO(pg.get_pixmap(dpi=250).tobytes("png"))
                            ),
                            lang="por",
                        )
                        for pg in doc
                    )
            disc = None
            m = re.search(r"PROVA ESCRITA DE ([A-Za-zÀ-ú ]{3,80})", native)
            if m:
                u = m.group(1).strip().upper()
                for pat, d in [
                    ("PORTUGU", "Língua Portuguesa"),
                    ("INGL", "Língua Inglesa"),
                    ("ESPANH", "Espanhol e Francês"),
                    ("FRANC", "Espanhol e Francês"),
                    ("ALEM", "Alemão"),
                    ("HIST", "História do Brasil"),
                    ("GEOGRAF", "Geografia"),
                    ("DIREITO", "Direito"),
                    ("ECONOM", "Economia"),
                    ("POL", "Política Internacional"),
                ]:
                    if pat in u:
                        disc = d
                        break
            if disc is None:
                disc = {
                    "Segunda_Fase_Port_Escr": "Língua Portuguesa",
                    "Segunda_Fase_Ingles_Escr": "Língua Inglesa",
                    "prova_disc_port": "Língua Portuguesa",
                    "prova_disc_ing": "Língua Inglesa",
                    "IRBR_001_1": "Língua Portuguesa",
                    "IRBR_001_2": "Língua Inglesa",
                    "IRBR_001_3": "História do Brasil",
                    "IRBr_001_4": "Geografia e Política Internacional",
                    "IRBR_DIPLOMACIA_001_1": None,
                    "IRBR_PROVA ESCRITA_ FRANCES": "Espanhol e Francês",
                    "IRBR_PROVA ESCRITA_ALEMAO": "Alemão",
                    "IRBR_PROVA ESCRITA_ESPANHOL": "Espanhol e Francês",
                    "IRBR_ECONOMIA": "Economia",
                    "IRBR_DIREITO_INTERNACIONAL_PUBLICO": "Direito",
                    "IRBR_GEOGRAFIA": "Geografia",
                    "IRBR_HISTORIA DO BRASIL": "História do Brasil",
                    "IRBR_INGLES": "Língua Inglesa",
                    "IRBR_POLIT_INTERNAC": "Política Internacional",
                    "IRBr_PORTUGUES_21_2_2010": "Língua Portuguesa",
                    "IRBR_ESPANHOL": "Espanhol e Francês",
                    "IRBR_FRANCES": "Espanhol e Francês",
                }.get(pdf.stem.strip())

            stage = "segunda_fase"
            phase = 2
            if re.search(r"3A|TERCEIRA", pdf.stem.upper()):
                stage = "terceira_fase"
                phase = 3

            qs = sorted(
                (m.start(), int(m.group(1)))
                for m in re.finditer(r"QUEST[ÃA]O\s+(\d{1,2})", native, re.I)
            )
            if qs:
                for idx, (pos, qn) in enumerate(qs):
                    end = qs[idx + 1][0] if idx + 1 < len(qs) else len(native)
                    text = norm(native[pos:end])
                    if len(text) < 80:
                        continue
                    is_essay = bool(
                        RE_ESSAY := re.search(
                            r"Extens[ãa]o m[áa]xima|valor", text, re.I
                        )
                    )
                    recs.append(
                        {
                            "contest_id": f"CACD_{y}",
                            "year": y,
                            "phase": phase,
                            "stage": stage,
                            "discipline": disc,
                            "question_number": qn,
                            "item_number": None,
                            "question_type": "essay" if is_essay else "certo_errado",
                            "question_text": text,
                            "item_text": None,
                            "alternatives": None,
                            "answer": None,
                            "page": None,
                            "caderno": None,
                            "source_file": str(pdf).replace("\\", "/"),
                            "source_url": None,
                            "confidence": 0.6,
                            "notes": "extracao automatica do zip archive.org",
                        }
                    )
            else:
                # sem QUESTAO: emite bloco inteiro como essay
                body = norm(native)
                if len(body) > 200:
                    recs.append(
                        {
                            "contest_id": f"CACD_{y}",
                            "year": y,
                            "phase": phase,
                            "stage": stage,
                            "discipline": disc,
                            "question_number": 1,
                            "item_number": None,
                            "question_type": "essay",
                            "question_text": body,
                            "item_text": None,
                            "alternatives": None,
                            "answer": None,
                            "page": None,
                            "caderno": None,
                            "source_file": str(pdf).replace("\\", "/"),
                            "source_url": None,
                            "confidence": 0.5,
                            "notes": "extracao automatica do zip (sem marcadores de questao)",
                        }
                    )
        if not recs:
            continue
        vistos, unicos = set(), []
        for r in recs:
            k = (r["discipline"], r["question_number"], r["question_text"][:60])
            if k not in vistos:
                vistos.add(k)
                unicos.append(r)
        recs = unicos
        out = folder / f"discursivas_faltantes_{y}.jsonl"
        with out.open("w", encoding="utf-8") as fh:
            for r in recs:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"[ok] {out.name}: {len(recs)} registros")
        total += len(recs)
    print(f"[total] {total} registros")


if __name__ == "__main__":
    main()
