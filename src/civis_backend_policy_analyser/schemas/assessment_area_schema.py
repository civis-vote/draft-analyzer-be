from datetime import datetime

from pydantic import Field

from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema


class AssessmentAreaBase(BaseModelSchema):
    assessment_name: str | None = None
    description: str | None = None
    prompt_ids: list[int] | None = Field(default_factory=list)
    summary_prompt: int | None = None

class AssessmentAreaCreate(AssessmentAreaBase):
    created_by: str | None = None

class AssessmentAreaUpdate(AssessmentAreaBase):
    updated_by: str | None = None

class AssessmentAreaOut(AssessmentAreaBase):
    assessment_id: int
    created_by: str | None
    created_on: datetime | None
    updated_by: str | None
    updated_on: datetime | None

    model_config = {
        "from_attributes": True
    }