from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

class DocumentChunker:
    @staticmethod
    def chunk_document(text, chunk_size=1000, chunk_overlap=150):
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_text(text)
        logger.info(f"Documents have been split into {len(chunks)} chunks.")
        return chunks