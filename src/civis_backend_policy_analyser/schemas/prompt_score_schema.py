
from datetime import datetime

from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema


class PromptScoreSchemaOut(BaseModelSchema):
    prompt_score_id: int | None = None
    assessment_summary_id: int
    prompt_id: int
    prompt_score: float | None = None
    max_score: int | None = None
    score_justification: str | None = None
    reference: str | None = None

    model_config = {
        "from_attributes": True
    }

class PromptScoreSchema(PromptScoreSchemaOut):
    created_on: datetime | None = None
    created_by: str | None = None

    model_config = {
        "from_attributes": True
    }
