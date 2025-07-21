from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from typing import List, Optional
from datetime import datetime

class PromptAnalysis(BaseModelSchema):
    description: str
    justification: str

class DocumentScoreOut(BaseModelSchema):
    assessment_id: str
    summary: str
    score: float
    prompt_analysis: List[PromptAnalysis]

class DocumentScoreSchema(BaseModelSchema):
    score_id: Optional[int] = None
    doc_id: str
    assessment_id: str
    prompt_id: str
    prompt_score: Optional[float] = None
    max_score: Optional[int] = None
    score_justification: Optional[str] = None
    created_on: Optional[datetime] = None
    created_by: Optional[str] = None
