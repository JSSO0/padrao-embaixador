"""Loader de documentos PDF ciente de colunas.

A extracao linear (Etapa 4) intercala colunas em cadernos 2-colunas (IADES).
Aqui re-extraimos via get_text("blocks") e agrupamos blocos por coluna
(clusters de x0), concatenando coluna esquerda -> direita, topo -> base.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

# palavras que caracterizam documento NAO-de-provas (editais, resultados, relacoes)
NON_EXAM_PATTERNS = re.compile(
    r"(?i)(lista de isen|resultado|convoca|demanda de candidatos|atendimento especia"
    r"|isen[çc][ãa]o de taxa|rela[çc][ãa]o provis|rela[çc][ãa]o final|comunica[çc]o|edital|parecer|demanda)",
)


@dataclass
class LoadedDoc:
    pdf_path: Path
    contest_id: str
    family: str
    source_file: str  # relativo ao root
    source_type: str = "secondary_repository"
    text: str = ""  # texto com colunas resolvidas
    linear_text: str = ""  # texto linear (get_text simple) p/ comparacao
    n_pages: int = 0
    blocks_per_page: list[list[tuple[float, float, str]]] = field(default_factory=list)


def load_manifest() -> dict[str, dict]:
    """URL -> linha do download_manifest (para source_type)."""
    path = RAW / "download_manifest.csv"
    out: dict[str, dict] = {}
    if not path.exists():
        return out
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("ok") == "1" and r.get("url"):
                out[r["url"]] = r
    return out


def source_type_for(pdf_path: Path, manifest: dict[str, dict]) -> str:
    fam = pdf_path.parent.name
    if fam == "cebraspe":
        return "official_cebraspe"
    if fam == "wayback":
        return "official_cebraspe_archive"
    if fam == "mre":
        return "official_mre"
    return "secondary_repository"


def cluster_columns(blocks: list[dict], page_width: float) -> list[list[dict]]:
    """Separa blocos em 1 ou 2 colunas APENAS se houver gutter real (nenhum
    bloco cruzando o meio). Retorna colunas ordenadas esquerda->direita."""
    if len(blocks) < 6:
        return [sorted(blocks, key=lambda b: (b[1], b[0]))]
    for frac in (0.50, 0.48, 0.52, 0.45, 0.55):
        cut = page_width * frac
        left = [b for b in blocks if b[2] <= cut]
        right = [b for b in blocks if b[0] >= cut]
        crossing = [b for b in blocks if b[0] < cut < b[2]]
        if len(left) >= 3 and len(right) >= 3 and len(crossing) == 0:
            return [
                sorted(left, key=lambda b: (b[1], b[0])),
                sorted(right, key=lambda b: (b[1], b[0])),
            ]
    return [sorted(blocks, key=lambda b: (b[1], b[0]))]


def load_pdf(pdf_path: Path, root: Path) -> LoadedDoc:
    doc = LoadedDoc(
        pdf_path=pdf_path,
        contest_id=pdf_path.relative_to(root / "data" / "raw").parts[0],
        family=pdf_path.parent.name,
        source_file=str(pdf_path.relative_to(root)),
    )
    pdf = pymupdf.open(pdf_path)
    doc.n_pages = pdf.page_count
    linear_parts: list[str] = []
    for page in pdf:
        pw = page.rect.width
        raw_blocks = []
        for b in page.get_text("blocks"):
            x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
            text = text.strip()
            if text:
                raw_blocks.append((x0, y0, x1, y1, text))
        cols = cluster_columns(raw_blocks, pw)
        page_blocks = []
        for col in cols:
            for x0, y0, x1, y1, text in col:
                page_blocks.append((round(x0, 1), round(y0, 1), text))
        doc.blocks_per_page.append(page_blocks)
        linear_parts.append(page.get_text("text"))
        doc.text += "\n".join(b[2] for b in page_blocks) + "\n"
    pdf.close()
    doc.linear_text = "\n".join(linear_parts)
    return doc


def looks_like_exam(doc: LoadedDoc) -> bool:
    """Heuristica: descarta editais/relacoes/resultado que cairam na pasta."""
    sample = doc.text[:3000].lower()
    if (
        NON_EXAM_PATTERNS.search(sample)
        and "prova objetiva" not in sample
        and "questão" not in sample
        and "questao" not in sample
    ):
        return False
    return True


def load_catalog_index() -> dict[str, dict]:
    """Arquivo -> (doc_type, source_type) a partir dos catalogos de metadata."""
    out: dict[str, dict] = {}
    for name in [
        "source_catalog.csv",
        "wayback_archive.csv",
        "curso_cacd_full.csv",
        "secondary_sources.csv",
    ]:
        p = ROOT / "data" / "metadata" / name
        if not p.exists():
            continue
        with p.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                url = (r.get("url") or r.get("wayback_url") or "").strip()
                if url:
                    out.setdefault(url, r)
    return out
