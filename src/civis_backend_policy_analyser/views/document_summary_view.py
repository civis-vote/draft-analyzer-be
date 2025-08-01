from loguru import logger
from sqlalchemy import select
from civis_backend_policy_analyser.core.document_agent_factory import LLMClient, create_document_agent
from civis_backend_policy_analyser.models.document_summary import DocumentSummary
from civis_backend_policy_analyser.models.prompt import Prompt
from civis_backend_policy_analyser.schemas.document_summary_schema import DocumentSummaryResponseSchema, DocumentSummarySchema
from civis_backend_policy_analyser.utils.constants import LLM_CLIENT
from civis_backend_policy_analyser.views.base_view import BaseView


class DocumentSummaryView(BaseView):
    model = DocumentSummary
    schema = DocumentSummarySchema

    async def summarize_document(self, doc_summary_id) -> DocumentSummaryResponseSchema:

        document_summary: DocumentSummary = await self.get(doc_summary_id)
        if not document_summary:
            raise ValueError(f"DocumentSummary with ID {doc_summary_id} not found")
        
        query_result = await self.db_session.execute(
            select(Prompt).filter(Prompt.prompt_type == 'DOCUMENT_SUMMARY')
        )
        summary_prompt: Prompt = query_result.scalars().first()
        if not summary_prompt:
            raise ValueError(f"Document Summary prompt not found in prompt table")

        agent = create_document_agent(client=LLMClient(LLM_CLIENT), document_id=document_summary.doc_id)

        logger.info(f"started fetching summary from LLM for document id: {document_summary.doc_id}")
        summary = agent.summarize(summary_prompt=summary_prompt.technical_prompt)
        logger.info(f"fetched summary from LLM: {summary}")
        
        if not summary:
            raise ValueError(f"No summary found for document ID: {document_summary.doc_id}")
        
        # Update the document summary with the fetched summary
        document_summary.summary_text = summary
        await self.db_session.commit()

        return DocumentSummaryResponseSchema.model_validate(document_summary)