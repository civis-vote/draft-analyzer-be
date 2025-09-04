from civis_backend_policy_analyser.config.logging_config import logger
from sqlalchemy import select

from civis_backend_policy_analyser.core.document_agent_factory import (
    LLMClient,
    create_document_agent,
)
from civis_backend_policy_analyser.models.assessment_area_summary import (
    AssessmentAreaSummary,
)
from civis_backend_policy_analyser.models.document_summary import DocumentSummary
from civis_backend_policy_analyser.models.evaluation_status import EvaluationStatus
from civis_backend_policy_analyser.models.prompt import Prompt
from civis_backend_policy_analyser.schemas.document_summary_schema import (
    DocumentSummarySchema,
)
from civis_backend_policy_analyser.schemas.executive_summary_schema import ExecutiveSummarySchema
from civis_backend_policy_analyser.schemas.executive_summary_schema import ExecutiveSummarySchema
from civis_backend_policy_analyser.utils.constants import LLM_CLIENT
from civis_backend_policy_analyser.utils.utils import strip_html_tags
from civis_backend_policy_analyser.views.base_view import BaseView


class ExecutiveSummaryView(BaseView):
    model = DocumentSummary
    schema = DocumentSummarySchema

    async def summarize_assessment_summaries(self, doc_summary_id) -> ExecutiveSummarySchema:

        document_summary: DocumentSummary = await self.db_session.get(DocumentSummary, doc_summary_id)
        if not document_summary:
            raise ValueError(f"DocumentSummary with ID {doc_summary_id} not found")
        
        if document_summary.executive_summary_text:
            logger.info(f"Executive summary already exists for document summary ID {doc_summary_id}. Returning existing summary.")
            return ExecutiveSummarySchema.model_validate(document_summary)
        
        query_result = await self.db_session.execute(
            select(Prompt).filter(Prompt.prompt_type == 'EXECUTIVE_SUMMARY')
        )
        summary_prompt: Prompt = query_result.scalars().first()
        if not summary_prompt:
            raise ValueError("Document Summary prompt not found in prompt table")

        fetch_assessments_summary_stmt = select(AssessmentAreaSummary.summary_text).where(
            AssessmentAreaSummary.doc_summary_id == doc_summary_id
        )
        assessments_summary_result = await self.db_session.execute(fetch_assessments_summary_stmt)
        summaries = assessments_summary_result.scalars().all()

        assessment_summaries = ""
        for summary in summaries:
            assessment_summaries = assessment_summaries + " " + strip_html_tags(summary)

        agent = create_document_agent(client=LLMClient(LLM_CLIENT), document_id=document_summary.doc_id)

        logger.info(f"started fetching summary from LLM for document id: {document_summary.doc_id}")
        executive_summary = agent.summarize(summary_prompt=summary_prompt.technical_prompt+" "+assessment_summaries)
        logger.info("fetched summary from LLM")

        if not executive_summary:
            raise ValueError(f"No summary found for document ID: {document_summary.doc_id}")

        # update DB
        document_summary.executive_summary_text = executive_summary
        document_summary.evaluation_status = EvaluationStatus.EXECUTIVE_SUMMARIZED

        await self.db_session.commit()
        await self.db_session.refresh(document_summary)

        return ExecutiveSummarySchema.model_validate(document_summary)