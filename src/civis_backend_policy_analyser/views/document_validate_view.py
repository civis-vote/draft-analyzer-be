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
from civis_backend_policy_analyser.models.document_metadata import DocumentMetadata
from civis_backend_policy_analyser.models.document_type import DocumentType
from civis_backend_policy_analyser.models.prompt import Prompt
from sqlalchemy import text


class DocumentValidateView(BaseView):
    model = DocumentSummary
    schema = DocumentSummarySchema

    async def validate_document(self, doc_id) -> DocumentSummarySchema:
        
        # Fetch document and its type
        document = await self.db_session.get(DocumentMetadata, doc_id)
        document_type = await self.db_session.get(DocumentType, document.doc_type_id)
        validation_prompt = await self.db_session.get(Prompt, document_type.doc_validation_prompt)

        agent = create_document_agent(client=LLMClient(LLM_CLIENT), document_id=doc_id)
        validation_result = agent.validate(validation_prompt.technical_prompt)
        # Prepare response
        # You may want to parse validation_result to determine validity
        is_valid_document = "True" if "success" in validation_result.lower() else "False"
        # validity checks?
        validity_checks = [
            "Document Type Validator Succeeded" if is_valid_document == "True" else "Document Type Validator Failed",
            "Content Validator Succeeded" if is_valid_document == "True" else "Content Validator Failed"
        ]

        # If is_valid_document is False, cleanup the db content by doc_id
        if is_valid_document == "False":
            await self.db_session.execute(
                text("DELETE FROM document_summary WHERE document_id = :doc_id"),
                {"doc_id": doc_id}
            )
            await self.db_session.commit()

        # Update the Validation status in document_metadata table
        document.is_valid_document = is_valid_document
        await self.db_session.commit()

        # Build and return response as a model
        response = {
            "document_id": doc_id,
            "filename": document.file_name,
            "is_valid_document": is_valid_document,
            "validity_checks": validity_checks
        }
        return response