import json
import re
from datetime import datetime

from loguru import logger

from civis_backend_policy_analyser.core.document_agent_factory import (
    LLMClient,
    create_document_agent,
)
from civis_backend_policy_analyser.models.document_summary import DocumentSummary
from civis_backend_policy_analyser.models.document_type import DocumentType
from civis_backend_policy_analyser.models.prompt import Prompt
from civis_backend_policy_analyser.schemas.document_summary_schema import (
    DocumentSummaryBaseSchema,
    DocumentSummarySchema,
)
from civis_backend_policy_analyser.utils.constants import LLM_CLIENT
from civis_backend_policy_analyser.views.base_view import BaseView


class DocumentValidateView(BaseView):
    model = DocumentSummary
    schema = DocumentSummarySchema

    async def validate_document(self, doc_id: str, doc_type_id: int) -> DocumentSummaryBaseSchema:
        # Get document type and validation prompt
        document_type = await self.db_session.get(DocumentType, doc_type_id)
        if not document_type:
            raise ValueError(f"DocumentType with ID {doc_type_id} not found")

        prompt = await self.db_session.get(Prompt, document_type.doc_validation_prompt)
        if not prompt:
            raise ValueError(f"Validation Prompt with ID {document_type.doc_validation_prompt} not found")

        agent = create_document_agent(client=LLMClient(LLM_CLIENT), document_id=doc_id)
        llm_response = agent.validate(prompt.technical_prompt)

        if not llm_response:
            raise ValueError(f"No LLM response for validation of document ID: {doc_id}")

        logger.info(f"Validation response for document {doc_id}: {llm_response}")

        parsed_response = self._parse_llm_response(llm_response)

        is_valid_document: bool = parsed_response.get("is_valid_document", False)
        doc_valid_status_msg: str = parsed_response.get("doc_valid_status_msg", "")

        # Create DocumentSummary instance
        document_summary = DocumentSummary(
            doc_id=doc_id,
            doc_type_id=doc_type_id,
            is_valid_document=is_valid_document,
            doc_valid_status_msg=doc_valid_status_msg,
            created_on=datetime.now(),
            created_by="Admin"  # Update this later on
        )
        doc_summary = await self.create(document_summary)

        return DocumentSummaryBaseSchema.model_validate(doc_summary)

    def _parse_llm_response(self, llm_response: str) -> dict:
        """Extract JSON object from LLM markdown-wrapped response."""
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", llm_response, re.DOTALL)
        json_str = match.group(1) if match else llm_response
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise ValueError("Invalid LLM response format")
