from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from typing import Optional
from datetime import datetime

class DocumentSummarySchema(BaseModelSchema):
    doc_summary_id: Optional[int] = None
    document_id: str
    summary_text: str
    created_on: Optional[datetime] = None
    created_by: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
        