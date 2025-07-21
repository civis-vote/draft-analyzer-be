from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from typing import List, Optional
from datetime import datetime

class PromptScore(BaseModelSchema):
    prompt_id: int
    score: float
    justification: str

    model_config = {
        "from_attributes": True
    }

class DocumentScoreOut(BaseModelSchema):
    assessment_id: str
    summary: str
    overall_score: float
    prompt_scores: List[PromptScore]

    model_config = {
        "from_attributes": True
    }

class DocumentScoreSchema(BaseModelSchema):
    doc_id: str
    assessment_id: int
    prompt_id: int
    prompt_score: Optional[float] = None
    max_score: Optional[int] = None
    score_justification: Optional[str] = None
    created_on: Optional[datetime] = None
    created_by: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
