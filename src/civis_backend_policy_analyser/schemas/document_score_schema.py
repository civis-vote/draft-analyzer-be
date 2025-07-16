from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from typing import List, Optional
from datetime import datetime

class PromptJustification(BaseModelSchema):
    prompt_summary: str
    prompt_justification: str

class DocumentScoreOut(BaseModelSchema):
    assessment_area_name: str
    score: float
    prompt_analysis: List[PromptJustification]

class DocumentScoreSchema(BaseModelSchema):
    score_id: Optional[int] = None
    doc_id: str
    assessment_id: str
    prompt_id: str
    assessment_json: dict
    created_on: Optional[datetime] = None
    created_by: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
