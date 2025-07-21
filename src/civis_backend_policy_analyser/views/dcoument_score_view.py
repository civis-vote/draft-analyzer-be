from civis_backend_policy_analyser.views.base_view import BaseView
from civis_backend_policy_analyser.models.document_score import DocumentScore
from civis_backend_policy_analyser.schemas.document_score_schema import DocumentScoreSchema

from sqlalchemy import select
from civis_backend_policy_analyser.views.assessment_area_prompt_view import AssessmentAreaPromptView
from civis_backend_policy_analyser.models.prompt import Prompt
from civis_backend_policy_analyser.schemas.prompt_schema import PromptSchema

class DocumentScoreView(BaseView):
    model = DocumentScore
    schema = DocumentScoreSchema
    
    async def score_assessment_area(self, document_id, assessment_id):
        # get the prompts associated with the current assessment_id
        prompt_records = await self.fetch_score_prompts(assessment_id)
        # assess the prompts from the LLM
        raise NotImplementedError
    
    async def fetch_score_prompts(self, assessment_id):
        # get prompt ids from assessment_area_prompt table (mapping table)
        mapping_view = AssessmentAreaPromptView(self.db_session)
        mapping_records = await mapping_view.filter(assessment_id=assessment_id)
        prompt_ids = [record.prompt_id for record in mapping_records]
        # get the prompts for filtered prompt ids
        result = await self.db_session.execute(
            select(Prompt).where(Prompt.prompt_id).in_(prompt_ids)
        )
        prompt_objs = result.scalars().all()
        prompt_schema = PromptSchema()
        return [prompt_schema.from_orm(record) for record in prompt_objs]
    
    async def format_result(self, assessment_area_summary, assessment_score):
        raise NotImplementedError
