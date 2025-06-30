import fitz
from loguru import logger

from civis_backend_policy_analyser.core.extractor.document_extractor import DocumentExtractor

class PDFExtractor(DocumentExtractor):
    def extract_text(file_bytes, document_id):
        doc = fitz.open(filename=document_id, stream=file_bytes, filetype="pdf")
        number_of_pages = doc.page_count
        text = "\n".join(page.get_text() for page in doc)
        logger.info(f"Document content extraction done for document id: {document_id}")
        return text, number_of_pages