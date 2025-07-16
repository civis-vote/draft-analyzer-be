from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from typing import List, Optional
from datetime import datetime

class PromptAnalysis(BaseModelSchema):
    description: str
    justification: str

class DocumentScoreOut(BaseModelSchema):
    score: float
    prompt_analysis: List[PromptAnalysis]

class DocumentScoreSchema(BaseModelSchema):
    score_id: Optional[int] = None
    doc_id: str
    assessment_id: str
    prompt_id: str
    prompt_score: float
    max_score: int
    score_justification: str
    created_on: Optional[datetime] = None
    created_by: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
