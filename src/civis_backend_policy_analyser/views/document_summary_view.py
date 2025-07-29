from datetime import datetime

from loguru import logger
from civis_backend_policy_analyser.core.document_agent import DocumentAgent
from civis_backend_policy_analyser.core.document_agent_factory import LLMClient, create_document_agent
from civis_backend_policy_analyser.core.embeddings.azure_embedding import AzureEmbeddingModel
from civis_backend_policy_analyser.core.embeddings.ollama_embedding import OllamaEmbeddingModel
from civis_backend_policy_analyser.core.llm.azure_llm import AzureLLMModel
from civis_backend_policy_analyser.core.llm.ollama_llm import OllamaLLMModel
from civis_backend_policy_analyser.models.document_summary import DocumentSummary
from civis_backend_policy_analyser.models.document_type import DocumentType
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
        
        document_type_obj = await self.db_session.get(DocumentType, document_summary.doc_type_id)
        prompt_obj = await self.db_session.get(Prompt, document_type_obj.doc_summary_prompt)

        agent = create_document_agent(client=LLMClient(LLM_CLIENT), document_id=document_summary.doc_id)

        logger.info(f"started fetching summary from LLM for document id: {document_summary.doc_id}")
        summary = agent.summarize(summary_prompt=prompt_obj.technical_prompt)
        logger.info(f"fetched summary from LLM: {summary}")
        
        if not summary:
            raise ValueError(f"No summary found for document ID: {document_summary.doc_id}")
        
        # Update the document summary with the fetched summary
        document_summary.summary_text = summary
        await self.db_session.commit()

        return DocumentSummaryResponseSchema.model_validate(document_summary)