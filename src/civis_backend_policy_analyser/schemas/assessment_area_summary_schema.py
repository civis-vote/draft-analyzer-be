from datetime import datetime

from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from civis_backend_policy_analyser.schemas.prompt_score_schema import (
    PromptScoreSchemaOut,
)


class AssessmentAreaSummarySchema(BaseModelSchema):
    assessment_summary_id: int | None = None
    doc_summary_id: int
    assessment_id: int
    summary_text: str
    created_on: datetime | None = None
    created_by: str | None = None

    model_config = {
        "from_attributed": True
    }

class AssessmentAreaSummaryOut(BaseModelSchema):
    assessment_summary_id: int
    assessment_id: int
    summary: str
    overall_score: float
    prompt_scores: list[PromptScoreSchemaOut]

    model_config = {
        "from_attributes": True
    }