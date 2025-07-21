from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from typing import Optional
from datetime import datetime

class AssessmentAreaSummarySchema(BaseModelSchema):
    doc_id: str
    assessment_id: int
    summary_text: str
    created_on: Optional[str] = None
    created_by: Optional[str] = None

    model_config = {
        "from_attributed": True
    }
