"""Emite as questoes 38-39 de 2010 a partir do OCR do PARTE_I."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
t = (ROOT / "data/raw/CACD_2010/archive/ocr_parte_i_2010.md").read_text(
    encoding="utf-8"
)

m38 = t.index("QUESTÃO 38")
m39 = t.index("QUESTÃO 39")
end39 = t.index("UnB / CESPE", m39)
q38 = t[m38:m39]
q39 = t[m39:end39]

SRC = "data/raw/CACD_2010/archive/IRBR_PARTE_I_2010_CAD_A_manha.pdf"
recs = []


def norm(s: str) -> str:
    return " ".join(s.replace("\n", " ").split()).strip()


# --- q38: multipla escolha (5 alternativas A-E) ---
b = " ".join(q38.replace("\n", " ").split())
command38 = "Em relação à questão ambiental internacional, assinale a opção correta."
kws = [
    "As primeiras tentativas",
    "O Tratado Antártico",
    "A Conferência de Estocolmo",
    "O chamado Clube de Roma",
    "Estabelecido em 1972",
]
body = b.replace("QUESTÃO 38", "").replace(command38, "").strip()
pos = [body.index(kw) for kw in kws] + [len(body)]
alts = []
for i, kw in enumerate(kws):
    seg = body[pos[i] : pos[i + 1]].strip()
    alts.append(f"{'ABCDE'[i]}) {seg}")
recs.append(
    {
        "contest_id": "CACD_2010",
        "year": 2010,
        "phase": 1,
        "stage": "primeira_fase",
        "discipline": "Política Internacional",
        "question_number": 38,
        "item_number": None,
        "question_type": "multiple_choice",
        "question_text": command38,
        "item_text": None,
        "alternatives": " ".join(alts),
        "answer": None,
        "page": 13,
        "caderno": "A",
        "source_file": SRC,
        "source_url": None,
        "confidence": 0.7,
        "notes": "OCR (tesseract 5.4, por) — PARTE_I com encoding de glifos corrompido",
    }
)

# --- q39: C/E com 4 itens (as caixas () da prova viram split) ---
b39 = norm(" ".join(q39.split()))
prompt_end = b39.index("julgue C ou E") + len("julgue C ou E.")
command39 = b39[:prompt_end]
rest = b39[prompt_end:]
raw = re.split(r"\(\s*\)", rest)
items = [norm(i) for i in raw if len(norm(i)) > 30]
for itn, item in enumerate(items, 1):
    recs.append(
        {
            "contest_id": "CACD_2010",
            "year": 2010,
            "phase": 1,
            "stage": "primeira_fase",
            "discipline": "Geografia",
            "question_number": 39,
            "item_number": itn,
            "question_type": "certo_errado",
            "question_text": command39,
            "item_text": item,
            "alternatives": None,
            "answer": None,
            "page": 14,
            "caderno": "A",
            "source_file": SRC,
            "source_url": None,
            "confidence": 0.7,
            "notes": "OCR (tesseract 5.4, por) — PARTE_I com encoding de glifos corrompido",
        }
    )

out = ROOT / "data/raw/CACD_2010/archive/questoes_faltantes_2010.jsonl"
with out.open("w", encoding="utf-8") as fh:
    for r in recs:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"[ok] 2010: {len(recs)} registros -> {out.name}")
