from datetime import datetime

from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema


class DocumentSummaryBaseSchema(BaseModelSchema):
    doc_summary_id: int | None = None
    doc_id: str
    doc_type_id: int
    is_valid_document: bool
    doc_valid_status_msg: str | None = None
    
    model_config = {
        "from_attributes": True
    }

class DocumentSummarySchema(DocumentSummaryBaseSchema):
    summary_text: str | None = None
    created_on: datetime | None = None
    created_by: str | None = None

    model_config = {
        "from_attributes": True
    }

class DocumentSummaryResponseSchema(BaseModelSchema):
    doc_summary_id: int | None = None
    doc_id: str
    summary_text: str | None = None

    model_config = {
        "from_attributes": True
    }

class DocumentValidateLLMResponse:
    is_valid_document: bool
    doc_valid_status_msg: str | None = None

class DocumentReportOut(BaseModelSchema):
    generated_report: str