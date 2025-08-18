from civis_backend_policy_analyser.views.base_view import BaseView
from civis_backend_policy_analyser.models.assessment_area_prompt import AssessmentAreaPrompt
from civis_backend_policy_analyser.schemas.assessment_area_prompt_schema import AssessmentAreaPromptSchema

class AssessmentAreaPromptView(BaseView):
    model = AssessmentAreaPrompt
    schema = AssessmentAreaPromptSchema
