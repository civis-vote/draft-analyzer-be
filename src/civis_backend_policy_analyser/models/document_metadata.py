from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
import datetime

from civis_backend_policy_analyser.models.base import Base


class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    doc_id = Column(String, primary_key=True, index=True)  # SHA-256 hash
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.datetime.now())
    number_of_pages = Column(Integer)
    doc_size_kb = Column(Integer)
