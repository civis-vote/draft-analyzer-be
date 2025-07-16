from sqlalchemy import Column, String, Text, Integer, Float, TIMESTAMP, func, ForeignKey
from civis_backend_policy_analyser.models.base import Base

class DocumentScore(Base):
    __tablename__ = "document_score"

    score_id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(String(100), ForeignKey('document_metadata.doc_id', ondelete='CASCADE'), nullable=False)
    assessment_id = Column(Integer, ForeignKey('assessment_area.assessment_id', ondelete='CASCADE'), nullable=False)
    prompt_id = Column(Integer, ForeignKey('prompt.prompt_id', ondelete='CASCADE'), nullable=False)
    prompt_score = Column(Float, nullable=False)
    max_score = Column(Integer, nullable=False)
    score_justification = Column(Text, nullable=False)
    created_on = Column(TIMESTAMP, default=func.now())
    created_by = Column(String(100))
