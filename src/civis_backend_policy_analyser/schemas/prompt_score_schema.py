
from datetime import datetime
from typing import Optional
from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema

class PromptScoreSchemaOut(BaseModelSchema):
    prompt_score_id: Optional[int] = None
    assessment_summary_id: int
    prompt_id: int
    prompt_score: Optional[float] = None
    max_score: Optional[int] = None
    score_justification: Optional[str] = None
    reference: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class PromptScoreSchema(PromptScoreSchemaOut):
    created_on: Optional[datetime] = None
    created_by: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class PromptScoreEvaluationSchema(BaseModelSchema):
    assessment_id: Optional[int] = None
    prompt_id: int
    criteria: Optional[str] = None
    prompt_score: Optional[float] = None
    max_score: Optional[int] = 5

    model_config = {
        "from_attributes": True
    }
