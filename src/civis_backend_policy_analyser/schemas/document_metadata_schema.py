from datetime import datetime
from typing import Optional

from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema


class DocumentMetadataBase(BaseModelSchema):
    doc_id: str
    file_name: str
    file_type: str
    upload_time: datetime
    number_of_pages: int
    doc_size_kb: int

class DocumentMetadataOut(DocumentMetadataBase):
    warning: str | None = None
    new_document: Optional["DocumentMetadataBase"] = None


    class Config:
        orm_mode = True
