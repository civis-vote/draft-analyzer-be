import io

from docx import Document

from civis_backend_policy_analyser.core.extractor.document_extractor import (
    DocumentExtractor,
)


class DOCXExtractor(DocumentExtractor):
    def extract_text(self, file_bytes, document_id):
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        # DOCX doesn't have a native page count, so we estimate by section breaks or default to 1
        number_of_pages = len(doc.element.xpath('//w:sectPr')) or 1
        return text, number_of_pages