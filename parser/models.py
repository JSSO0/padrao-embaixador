"""Modelos de dominio da etapa 5 (Pydantic v2). Spec: docs/spec-etapa5.md"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

SourceType = Literal[
    "official_mre",
    "official_cebraspe",
    "official_cebraspe_archive",
    "secondary_repository",
    "unknown",
]
QuestionType = Literal["multiple_choice", "certo_errado", "essay"]
ExtractionMethod = Literal["rules", "manual"]

SOURCE_PRIORITY = {
    "official_cebraspe": 0,
    "official_cebraspe_archive": 1,
    "official_mre": 2,
    "secondary_repository": 3,
    "unknown": 9,
}


def question_id(
    contest_id: str,
    stage: str,
    discipline: str | None,
    question_number: int | None,
    item_number: int | None,
) -> str:
    """ID deterministico: reprocessar nao muda o id."""
    raw = f"{contest_id}|{stage}|{discipline or 'SEM_DISCIPLINA'}|{question_number or 0}|{item_number or 0}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


class Alternative(BaseModel):
    letter: str
    text: str


class Item(BaseModel):
    item_number: int
    text: str
    answer: str | None = None
    confidence: float = 1.0


class Question(BaseModel):
    parent_question_id: str | None = None
    question_id: str
    contest_id: str
    year: int
    phase: int
    stage: str
    discipline: str | None = None
    question_number: int | None = None
    item_number: int | None = None
    item_text: str | None = None
    question_type: QuestionType
    question_text: str = ""
    alternatives: list[Alternative] = []
    answer: str | None = None
    items: list[Item] = []
    source_url: str | None = None
    source_type: SourceType
    source_file: str
    page: int | None = None
    extraction_method: ExtractionMethod = "rules"
    warnings: list[str] = []


class DocumentContext(BaseModel):
    """Documento carregado (texto com colunas resolvidas + metadados)."""

    contest_id: str
    family: str
    year: int
    source_file: str
    source_type: SourceType
    source_url: str | None = None
    doc_role: Literal["prova", "gabarito", "padrao_resposta", "edital", "outro"] = (
        "prova"
    )
    pages: list[list[tuple[float, float, str]]] = Field(
        default_factory=list
    )  # (x0,y0,text) por pagina
    text: str = ""
    n_pages: int = 0
    loaded_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @classmethod
    def from_pdf_path(
        cls, pdf_path: Path, root: Path, manifest: dict
    ) -> "DocumentContext":
        contest = pdf_path.relative_to(root / "data" / "raw").parts[0]
        family = pdf_path.parent.name
        year = (
            int(contest.replace("CACD_", "").split("_")[0])
            if contest.startswith("CACD_")
            else 0
        )
        return cls(
            contest_id=contest,
            family=family,
            year=year,
            source_file=str(pdf_path.relative_to(root)),
            source_type=manifest.get("source_type", "secondary_repository"),
            source_url=manifest.get("url"),
            doc_role="gabarito" if "gabarito" in pdf_path.stem.lower() else "prova",
        )


class ParsedExam(BaseModel):
    contest_id: str
    source_file: str
    family: str
    questions: list[Question] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ExtractionReport(BaseModel):
    contest_id: str
    source_file: str
    family: str
    parser: str = ""
    questions_found: int = 0
    questions_expected: int | None = None
    expected_unknown: bool = True
    coverage: float | None = None
    duplicate_of: str | None = None
    skipped: bool = False
    reason: str = ""
    issues: list[str] = Field(default_factory=list)
