from pydantic import Field
from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from typing import List, Optional
from datetime import datetime

class AssessmentAreaBase(BaseModelSchema):
    assessment_name: Optional[str] = None
    description: Optional[str] = None
    prompt_ids: Optional[List[int]] = Field(default_factory=list)

class AssessmentAreaCreate(AssessmentAreaBase):
    created_by: Optional[str] = None

class AssessmentAreaUpdate(AssessmentAreaBase):
    updated_by: Optional[str] = None

class AssessmentAreaOut(AssessmentAreaBase):
    assessment_id: int
    created_by: str
    created_on: Optional[datetime]
    updated_by: Optional[str]
    updated_on: Optional[datetime]

    model_config = {
        "from_attributes": True
    }