
from typing import Optional, List
from datetime import datetime
from pydantic import Field

from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema


class DocumentTypeBase(BaseModelSchema):
    doc_type_name: Optional[str] = None
    description: Optional[str] = None
    assessment_ids: Optional[List[int]] = Field(default_factory=list)

class DocumentTypeCreate(DocumentTypeBase):
    created_by: Optional[str] = None

class DocumentTypeUpdate(DocumentTypeBase):
    updated_by: Optional[str] = None

class DocumentTypeOut(DocumentTypeBase):
    doc_type_id: int
    created_by: str
    created_on: Optional[datetime]
    updated_by: Optional[str]
    updated_on: Optional[datetime]

    model_config = {
        "from_attributes": True
    }
