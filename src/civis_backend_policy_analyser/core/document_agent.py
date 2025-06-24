import uuid
import fitz
from loguru import logger

from langchain_text_splitters import RecursiveCharacterTextSplitter

from civis_backend_policy_analyser.core.model import get_rag_chain
from civis_backend_policy_analyser.core.vector_db_store import VectorDB


class DocumentAgent:
    """
    RAG-powered processor for summarization, assessment, and executive generation
    using Azure-hosted DeepSeek R1 via LangChain + PGVector.

    DocumentAgent orchestrates the full document processing workflow:
    - PDF ingestion and extraction
    - Semantic and agentic chunking
    - Vector storage with PGVector
    - DeepSeek-based summarization and assessment
    - Cleanup operations

    Attributes:
        vector_store (VectorDB): Backend PGVector client
        doc_chunks (dict): Cached document chunks by doc ID
        doc_raw_text (dict): Cached raw document content by doc ID
    """
    def __init__(self, document_id = None):
        """
        Instantiating a DocumentAgent to create a content or run the queries on the content.

        Args:
            document_id (str): Value is based on the request type.
                - If user is querying on the data then `document_id` should be present.
                - If user is creating external data soure, then it'll return the generate the `document_id`.

        """
        self.document_id = str(uuid.uuid4()) if not document_id else document_id
        logger.info(f"Vectore Store Document Id: {self.document_id}")
        self.vector_store = VectorDB(self.document_id)

    def load_and_chunk(self, upload_file):
        """
        Ingests a document upload, extracts the text, chunks it, and stores vectors.
        Args:
            upload_file (UploadFile): A FastAPI file upload object (PDF)
        Returns:
            str: Unique document ID for downstream retrieval
        """
        content = upload_file.read()
        text = self.__extract_text_from_pdf(self.document_id, content)
        logger.info(f"Document content extraction done.")

        document_chunks = self.__chunk_document(text)
        self.vector_store.store_embedding(document_chunks)
        logger.info("Document chunks has been embedded successfully to the vector store.")
        return {"document_id": self.document_id}

    @staticmethod
    def __extract_text_from_pdf(document_id, file_bytes):
        """
        Extracts plain text from a binary PDF file.

        Args:
            file_bytes (bytes): Raw PDF content

        Returns:
            str: Full extracted text from all pages
        """
        doc = fitz.open(filename=document_id, stream=file_bytes, filetype="pdf")
        return "\n".join(page.get_text() for page in doc)

    @staticmethod
    def __chunk_document(text):
        """
        Performs semantic and recursive chunking of document text.

        Args:
            text (str): Full document content

        Returns:
            list: List of individual text chunks
        """
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = splitter.split_text(text)
        logger.info(f"Documents have been splitted in to {len(chunks)} chunks.")
        return chunks

    def summarize(self, summary_prompt: str = "Summarize this:"):
        """
        Summarizes all the chunks associated with a document.

        Returns:
            str: Combined LLM-generated summary
        """
        rag_chain = get_rag_chain(retriever=self.vector_store.retriever)
        result = rag_chain.run(summary_prompt)
        return result

    def assess(self, prompts: list[str]):
        """
        Performs retrieval-based assessment for each prompt.

        Returns:
            dict: Prompt → generated output
        """
        rag_chain = get_rag_chain(retriever=self.vector_store.retriever)
        return {prompt: rag_chain.invoke(prompt) for prompt in prompts}

    def cleanup(self):
        """
        Deletes all associated vector data and cache from memory/storage.

        Args:
            doc_id (str): Identifier of the document to remove
        """
        self.vector_store.delete_all_vectors()

    @staticmethod
    def __execution_summary_context(self, iterator_object: list, format_string: str):
        return "\n\n".join([format_string.format(**kwargs) for kwargs in iterator_object])

    def execution_summary(self, exec_summary_prompt, context):
        rag_chain = get_rag_chain()

        assessment_context = ""
        assessment_title_string = "Area of Assessment: {assessment_title}\n\n"
        assessment_area_string = "{prompt_title}:\n Result: {result} \n\n"

        for assessment in context["assessment_areas"]:
            assessment_context += self.__execution_summary_context([assessment], assessment_title_string)
            assessment_context += self.__execution_summary_context(
                assessment["assessment_result"], assessment_area_string
            )
        summary_result = context["summary_result"]

        prompt = f"""
        {exec_summary_prompt}\n\n
        Summary: {summary_result} \n\n
        Document Assessment Details: \n\n {assessment_context}\n
        """
        result = rag_chain.run(prompt)
        return result
