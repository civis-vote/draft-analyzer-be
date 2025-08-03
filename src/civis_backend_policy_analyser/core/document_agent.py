import uuid
from fastapi import UploadFile
from loguru import logger

from civis_backend_policy_analyser.core.agent.document_chunker import DocumentChunker
from civis_backend_policy_analyser.core.extractor.document_extractor import DocumentExtractor
from civis_backend_policy_analyser.core.agent.summarizer import DocumentSummarizer
from civis_backend_policy_analyser.core.agent.vector_store import DocumentVectorStore
from civis_backend_policy_analyser.core.embeddings.base_embedding import BaseEmbeddingModel
from civis_backend_policy_analyser.core.llm.base_llm import BaseLLMModel
from civis_backend_policy_analyser.core.model import get_rag_chain


class DocumentAgent:

    def __init__(self, embedding_model: BaseEmbeddingModel, llm_model: BaseLLMModel, document_id=None):
        self.document_id = str(uuid.uuid4()) if not document_id else document_id
        self.vector_store = DocumentVectorStore(self.document_id, embedding_model)
        self.llm_model = llm_model

    async def load_and_chunk(self, upload_file: UploadFile):
       
        content = await upload_file.read()

        extractor: DocumentExtractor = DocumentExtractor.get_extractor(upload_file)

        text, number_of_pages = extractor.extract_text(content, self.document_id)
        
        size_kb = round(len(content) / 1024, 2)
        logger.info("document size in kb: ", size_kb)

        document_chunks = DocumentChunker.chunk_document(text)
        
        self.vector_store.store_embedding(document_chunks)
        logger.info("Document chunks has been embedded successfully to the vector store.")

        return {"document_id": self.document_id, "size_kb": size_kb, "number_of_pages": number_of_pages}

    def summarize(self, summary_prompt="Summarize this document and return result in nice presentable html format"):

        # summary_prompt = """
        # You are a summarization assistant. Your task is to summarize documents concisely and professionally.
        #     Instructions:
        #     - Only include factual, useful information from the input.
        #     - Do not include phrases like "Thinking...", "Let's see", or "As an AI".
        #     - Do not explain your reasoning.
        #     - Keep the summary objective and direct.
        #     - return result in nice presentable html format
        #     Now summarize the following content:
        # """
        summarizer = DocumentSummarizer(self.vector_store.retriever, self.llm_model)
        return summarizer.summarize(summary_prompt)

    def assess(self, prompts: list[str]):
        expected_format_instructions = """
        """
        summarizer = DocumentSummarizer(self.vector_store.retriever, self.llm_model)
        return summarizer.assess(prompts, expected_format_instructions)
    
    def validate(self, validation_prompt: str):
        expected_format_instructions = """
            You are a document validation assistant. Your task is to validate the documents.
            Instructions:
            - Return the validation result strictly in a structured JSON format as follows:
            {
                "is_valid_document": true/false,
                "doc_valid_status_msg": "Your validation message here"
            }
            """
        validation_prompt = expected_format_instructions + validation_prompt
        validator = DocumentSummarizer(self.vector_store.retriever, self.llm_model)
        return validator.summarize(validation_prompt)

    def cleanup(self):
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