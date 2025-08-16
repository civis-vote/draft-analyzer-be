from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from typing import List, Optional
from datetime import datetime

class AssessmentAreaSummarySchema(BaseModelSchema):
    assessment_summary_id: Optional[int] = None
    doc_summary_id: int
    assessment_id: int
    summary_text: str
    created_on: Optional[datetime] = None
    created_by: Optional[str] = None

    model_config = {
        "from_attributed": True
    }

class AssessmentAreaSummaryOut(BaseModelSchema):
    assessment_id: int
    summary: str
    overall_score: float

    model_config = {
        "from_attributes": True
    }