from civis_backend_policy_analyser.views.base_view import BaseView
from civis_backend_policy_analyser.models.assessment_area_summary import AssessmentAreaSummary
from civis_backend_policy_analyser.schemas.assessment_area_summary_schema import AssessmentAreaSummarySchema

from datetime import datetime
from loguru import logger
from civis_backend_policy_analyser.views.assessment_area_view import AssessmentAreaView
from civis_backend_policy_analyser.views.prompt_view import PromptView
from civis_backend_policy_analyser.utils.constants import LLM_CLIENT
from civis_backend_policy_analyser.core.document_agent_factory import LLMClient, create_document_agent

class AssessmentAreaSummaryView(BaseView):
    model = AssessmentAreaSummary
    schema = AssessmentAreaSummarySchema

    async def summarize_assessment_area(self, document_id, assessment_id):
        # fetch assessment area summary prompt
        summary_prompt = await self.fetch_summary_prompt(assessment_id)
        # create document agent and invoke LLM
        agent = create_document_agent(client=LLMClient(LLM_CLIENT), document_id=document_id)
        assessment_summary = agent.summarize(summary_prompt=summary_prompt)
        if not assessment_summary:
            raise ValueError(f"Could not summarize document {document_id} for assessment area {assessment_id}")
        logger.info(f"started fetching summary from LLM for document id: {document_id} and assessment id: {assessment_id}")
        summary_record = AssessmentAreaSummarySchema(
            assessment_id = assessment_id,
            summary_text = assessment_summary,
            created_on = datetime.now(),
            created_by = "Admin"
        )
        logger.info(f"fetching summary from LLM: {assessment_summary}")
        assessment_area_summary = await self.create(summary_record)
        return assessment_area_summary

    async def fetch_summary_prompt(self, assessment_id):
        # get prompt id from summary_prompt column in assessment_area table
        assessment_area_view = AssessmentAreaView(self.db_session)
        assessment_area_record = await assessment_area_view.filter(assessment_id=assessment_id)[0]
        summary_prompt_id = assessment_area_record.summary_prompt
        # get prompt for that id from the prompt table
        prompt_view = PromptView(self.db_session)
        prompt_record = await prompt_view.filter(prompt_id=summary_prompt_id)[0]
        summary_prompt = prompt_record.technical_prompt
        return summary_prompt
