import logging

from civis_backend_policy_analyser.core.extractor.document_extractor import DocumentExtractor

logger = logging.getLogger(__name__)

class TextExtractor(DocumentExtractor):
    def extract_text(self, file_bytes, document_id):
        """
        Extracts text from a plain .txt document.

        Args:
            file_bytes (bytes): Raw file content.
            document_id (str): Identifier or filename.

        Returns:
            tuple: (str: full text, int: number of pages simulated as lines/60)
        """
        try:
            # Decode bytes to string
            text = file_bytes.decode("utf-8")

            # page count by assuming ~60 lines per page
            lines = text.splitlines()
            number_of_pages = max(1, len(lines) // 60)

            logger.info(f"Document content extraction done for document id: {document_id}")
            return text, number_of_pages

        except UnicodeDecodeError:
            logger.error(f"Failed to decode text file: {document_id}")
            return "", 0
