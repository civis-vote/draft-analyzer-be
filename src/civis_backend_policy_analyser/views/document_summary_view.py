from datetime import datetime

from loguru import logger
from civis_backend_policy_analyser.core.document_agent import DocumentAgent
from civis_backend_policy_analyser.core.document_agent_factory import LLMClient, create_document_agent
from civis_backend_policy_analyser.core.embeddings.azure_embedding import AzureEmbeddingModel
from civis_backend_policy_analyser.core.embeddings.ollama_embedding import OllamaEmbeddingModel
from civis_backend_policy_analyser.core.llm.azure_llm import AzureLLMModel
from civis_backend_policy_analyser.core.llm.ollama_llm import OllamaLLMModel
from civis_backend_policy_analyser.models.document_summary import DocumentSummary
from civis_backend_policy_analyser.schemas.document_summary_schema import DocumentSummarySchema
from civis_backend_policy_analyser.utils.constants import LLM_CLIENT
from civis_backend_policy_analyser.views.base_view import BaseView


class DocumentSummaryView(BaseView):
    model = DocumentSummary
    schema = DocumentSummarySchema

    async def summarize_document(self, doc_id) -> DocumentSummarySchema:
        
        agent = create_document_agent(client=LLMClient(LLM_CLIENT), document_id=doc_id)
        
        summary = agent.summarize()
        if not summary:
            raise ValueError(f"No summary found for document ID: {doc_id}")
        logger.info(f"started fetching summary from LLM for document id: {doc_id}")
        document_summay = DocumentSummarySchema(
                document_id = doc_id,
                summary_text = summary,
                created_on = datetime.now(),
                created_by = "Admin" # update this later on
        )
        logger.info(f"fetched summary from LLM: {summary}")
        document_summay_response = await self.create(document_summay)

        return document_summay_response