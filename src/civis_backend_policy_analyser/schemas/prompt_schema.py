from datetime import datetime

from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema


class PromptSchema(BaseModelSchema):
    prompt_id: int | None = None
    prompt_type: str
    criteria: str
    description: str
    technical_prompt: str | None = None
    created_by: str
    created_on: datetime | None = None
    updated_by: str | None = None
    updated_on: datetime | None = None

    model_config = {
        "from_attributes": True
    }
