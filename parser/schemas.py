from __future__ import annotations

import pandera as pa
from pandera.typing import Series


class QuestionsSchema(pa.DataFrameModel):
    question_id: Series[str]
    parent_question_id: Series[str] | None = pa.Field(nullable=True)
    contest_id: Series[str]
    year: Series[int]
    phase: Series[int]
    stage: Series[str]
    discipline: Series[str] | None = pa.Field(nullable=True)
    question_number: Series[float] | Series[int] | None = pa.Field(nullable=True)
    item_number: Series[float] | Series[int] | None = pa.Field(nullable=True)
    question_type: Series[str] = pa.Field(isin=["multiple_choice", "certo_errado", "essay"])
    question_text: Series[str]
    item_text: Series[str] | None = pa.Field(nullable=True)
    alternatives: Series[str] | None = pa.Field(nullable=True)
    answer: Series[str] | None = pa.Field(nullable=True)
    source_type: Series[str]
    source_file: Series[str]
    extraction_method: Series[str] = pa.Field(default="rules")
    warnings: Series[str] | None = pa.Field(nullable=True)
