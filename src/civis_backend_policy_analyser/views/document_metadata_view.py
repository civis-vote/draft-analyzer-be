import os
import hashlib
import shutil
import fitz  # PyMuPDF
from datetime import datetime
from fastapi import UploadFile
from sqlalchemy import select
from loguru import logger

from civis_backend_policy_analyser.models.document_metadata import DocumentMetadata
from civis_backend_policy_analyser.schemas.document_metadata_schema import DocumentMetadataOut
from civis_backend_policy_analyser.views.base_view import BaseView

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class DocumentMetadataView(BaseView):
    model = DocumentMetadata
    schema = DocumentMetadataOut

    async def upload_policy_document(self, file: UploadFile) -> DocumentMetadata:
        if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            raise ValueError("Only PDF or DOCX files are supported")

        file_hash = self._compute_file_hash(file)
        extension = file.filename.split(".")[-1]
        saved_filename = f"{file_hash}.{extension}"
        file_path = os.path.join(UPLOAD_DIR, saved_filename)

        logger.info(f"Saving file to {file_path}")
        # Avoid duplicate file name override
        counter = 1
        while os.path.exists(file_path):
            base_name_only = f"{file_hash}_{counter}.{extension}"
            file_path = os.path.join(UPLOAD_DIR, base_name_only)
            counter += 1
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        stmt = select(DocumentMetadata).where(DocumentMetadata.doc_id == file_hash)
        result = await self.db_session.execute(stmt)
        existing = result.scalars().first()
        file_size_kb = os.path.getsize(file_path) // 1024
        number_of_pages = self._get_pdf_page_count(file_path)

        document = DocumentMetadata(
            doc_id=file_hash,
            file_name=file.filename,
            file_type=file.content_type,
            upload_time=datetime.now(),
            number_of_pages=number_of_pages,
            doc_size_kb=file_size_kb,
        )
        if existing:
            existing.warning = ("This document has already been uploaded.")
            # Append current timestamp in YYYYMMDDHHMMSS format
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            document.doc_id = f"{document.doc_id}_{timestamp}"
            existing.new_document = self.schema.from_orm(document)
            return existing
        
        # If no existing document, create a new one 
        await self.create(document)

        return document

    def _compute_file_hash(self, file_obj: UploadFile) -> str:
        hasher = hashlib.sha256()
        file_obj.file.seek(0)
        while chunk := file_obj.file.read(8192):
            hasher.update(chunk)
        file_obj.file.seek(0)
        return hasher.hexdigest()

    def _get_pdf_page_count(self, file_path: str) -> int:
        if file_path.endswith(".pdf"):
            with fitz.open(file_path) as doc:
                return doc.page_count
        # Optional: return None or 1 for DOCX if you support it later
        return 1
