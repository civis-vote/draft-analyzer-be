from datetime import datetime
from fastapi import UploadFile
from civis_backend_policy_analyser.config.logging_config import logger

from civis_backend_policy_analyser.core.document_agent_factory import LLMClient, create_document_agent
from civis_backend_policy_analyser.models.document_metadata import DocumentMetadata
from civis_backend_policy_analyser.models.document_summary import DocumentSummary
from civis_backend_policy_analyser.schemas.document_metadata_schema import DocumentMetadataOut
from civis_backend_policy_analyser.utils.constants import LLM_CLIENT
from civis_backend_policy_analyser.views.base_view import BaseView

class DocumentMetadataView(BaseView):
    model = DocumentMetadata
    schema = DocumentMetadataOut

    async def upload_policy_document(self, file: UploadFile) -> DocumentMetadata:
        if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            raise ValueError("Only PDF or DOCX files are supported")

        agent = create_document_agent(LLMClient(LLM_CLIENT))

        document_data = await agent.load_and_chunk(file)
        logger.info(f"Document {file.filename} has been processed and chunked with ID: {document_data['document_id']}")

        document = DocumentMetadata(
            doc_id=document_data['document_id'],
            file_name=file.filename,
            file_type=file.content_type,
            upload_time=datetime.now(),
            number_of_pages=document_data['number_of_pages'],
            doc_size_kb=document_data['size_kb'],
        )

        await self.create(document)

        return document

    async def clean_vector_db_store(self, doc_summary_id: int):
        """
        Clean up the vector database store for the given document summary id.
        This involves deleting all vectors associated with the document.
        """
        # Fetch the document summary to get doc_id
        document_summary = await self.db_session.get(DocumentSummary, doc_summary_id)
        if not document_summary:
            logger.warning(f"Document Summary with id {doc_summary_id} not found. Skipping vector DB cleanup.")
            return 
        document_id = document_summary.doc_id
        agent = create_document_agent(client=LLMClient(LLM_CLIENT), document_id=document_id)
        # Cleanup the vector store used by the agent for document id, if need to retain the vector store for future use, comment out the line below
        await agent.cleanup()
        logger.info(f"Cleaned up vector store for document id: {document_id}")