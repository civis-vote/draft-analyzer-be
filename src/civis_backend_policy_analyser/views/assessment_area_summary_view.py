from civis_backend_policy_analyser.views.base_view import BaseView
from civis_backend_policy_analyser.models.assessment_area_summary import AssessmentAreaSummary
from civis_backend_policy_analyser.schemas.assessment_area_summary_schema import AssessmentAreaSummarySchema

from datetime import datetime
from loguru import logger
from civis_backend_policy_analyser.models.assessment_area import AssessmentArea
from civis_backend_policy_analyser.models.prompt import Prompt
from civis_backend_policy_analyser.models.document_summary import DocumentSummary
from civis_backend_policy_analyser.utils.constants import LLM_CLIENT
from civis_backend_policy_analyser.core.document_agent_factory import LLMClient, create_document_agent

class AssessmentAreaSummaryView(BaseView):
    model = AssessmentAreaSummary
    schema = AssessmentAreaSummarySchema

    async def summarize_assessment_area(self, doc_summary_id: int, assessment_id: int) -> AssessmentAreaSummarySchema:
        # fetch assessment area summary prompt
        summary_prompt = await self.fetch_summary_prompt(assessment_id)
        # fetch doc_id from document_summary table
        document_summary: DocumentSummary = await self.db_session.get(DocumentSummary, id=doc_summary_id)
        if not document_summary:
            raise ValueError(f"Document Summary with id {doc_summary_id} not found")
        document_id = document_summary.doc_id
        # create document agent and invoke LLM
        agent = create_document_agent(client=LLMClient(LLM_CLIENT), document_id=document_id)
        assessment_summary = agent.summarize(summary_prompt=summary_prompt)
        if not assessment_summary:
            raise ValueError(f"Could not summarize document {document_id} for assessment area {assessment_id}")
        logger.info(f"started fetching summary from LLM for document id: {document_id} and assessment id: {assessment_id}")
        summary_record = AssessmentAreaSummary(
            doc_id = document_id,
            assessment_id = assessment_id,
            summary_text = assessment_summary,
            created_on = datetime.now(),
            created_by = "Admin"  # needs to be replaced with user_id
        )
        logger.info(f"fetched summary from LLM: {assessment_summary}")
        assessment_area_summary = await self.create(summary_record)
        return AssessmentAreaSummarySchema.model_validate(assessment_area_summary)

    async def fetch_summary_prompt(self, assessment_id: int) -> str:
        # get prompt id from summary_prompt column in assessment_area table
        assessment_area_record: AssessmentArea = await self.db_session.get(AssessmentArea, id=assessment_id)
        if not assessment_area_record:
            raise ValueError(f"Assessment area with id {assessment_id} not found")
        # get prompt for that id from the prompt table
        prompt_id = assessment_area_record.summary_prompt
        prompt_record: Prompt = await self.db_session.get(Prompt, id=prompt_id)
        if not prompt_record:
            raise ValueError(f"Prompt with id {prompt_id} not found")
        summary_prompt = prompt_record.technical_prompt
        return summary_prompt
