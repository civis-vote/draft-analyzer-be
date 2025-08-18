
from datetime import datetime

from pydantic import Field

from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema


class DocumentTypeBase(BaseModelSchema):
    doc_type_name: str | None = None
    description: str | None = None
    doc_validation_prompt: int | None = None
    assessment_ids: list[int] | None = Field(default_factory=list)

class DocumentTypeCreate(DocumentTypeBase):
    created_by: str | None = None

class DocumentTypeUpdate(DocumentTypeBase):
    updated_by: str | None = None

class DocumentTypeOut(DocumentTypeBase):
    doc_type_id: int
    created_by: str
    created_on: datetime | None
    updated_by: str | None
    updated_on: datetime | None

    model_config = {
        "from_attributes": True
    }
