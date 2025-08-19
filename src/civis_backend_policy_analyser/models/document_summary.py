from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, TIMESTAMP, func
from civis_backend_policy_analyser.models.base import Base

class DocumentSummary(Base):
    __tablename__ = "document_summary"

    doc_summary_id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(String(100), ForeignKey('document_metadata.doc_id'), nullable=False)
    doc_type_id = Column(Integer, ForeignKey('document_type.doc_type_id'), nullable=False)

    is_valid_document = Column(Boolean, nullable=True)
    doc_valid_status_msg = Column(Text, nullable=True)

    summary_text = Column(Text, nullable=True)
    report_file_name = Column(String(255), nullable=True)
    created_on = Column(TIMESTAMP, default=func.now())
    created_by = Column(String(100))
    executive_summary_text = Column(Text, nullable=True)

