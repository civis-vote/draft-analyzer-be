from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema

class AssessmentAreaPromptSchema(BaseModelSchema):
    assessment_id: int
    prompt_id: int
