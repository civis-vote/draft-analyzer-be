from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from typing import Optional
from datetime import datetime


class DocumentSummaryBaseSchema(BaseModelSchema):
    doc_summary_id: Optional[int] = None
    doc_id: str
    doc_type_id: int
    is_valid_document: bool
    doc_valid_status_msg: Optional[str] = None
    
    model_config = {
        "from_attributes": True
    }

class DocumentSummarySchema(DocumentSummaryBaseSchema):
    summary_text: Optional[str] = None
    executive_summary_text: Optional[str] = None
    created_on: Optional[datetime] = None
    created_by: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class DocumentSummaryResponseSchema(BaseModelSchema):
    doc_summary_id: Optional[int] = None
    doc_id: str
    summary_text: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class DocumentValidateLLMResponse():
    is_valid_document: bool
    doc_valid_status_msg: Optional[str] = None

class DocumentReportOut(BaseModelSchema):
    generated_report: str