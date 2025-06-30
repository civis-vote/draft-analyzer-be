from abc import ABC, abstractmethod

from fastapi import UploadFile

class DocumentExtractor(ABC):
    @abstractmethod
    def extract_text(self, file_bytes, document_id):
        pass

    @staticmethod
    def get_extractor(upload_file: UploadFile):
        from .pdf_extractor import PDFExtractor
        from .docx_extractor import DOCXExtractor
        # Add more imports as you add new extractors

        extractor_map = {
            "pdf": PDFExtractor,
            "docx": DOCXExtractor,
            # Add more mappings as needed
        }
        filename = upload_file.filename
        file_ext = filename.split('.')[-1].lower()

        extractor_cls = extractor_map.get(file_ext.lower())
        if not extractor_cls:
            raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")
        return extractor_cls()