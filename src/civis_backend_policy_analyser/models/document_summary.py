from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from civis_backend_policy_analyser.models.base import Base

class DocumentSummary(Base):
    __tablename__ = "document_summary"

    doc_summary_id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String(100), nullable=False, index=True)
    summary_text = Column(Text)
    created_on = Column(TIMESTAMP, default=func.now())
    created_by = Column(String(100))

