from sqlalchemy import Column, String, Text, Integer, Float, TIMESTAMP, func, ForeignKey
from civis_backend_policy_analyser.models.base import Base

class PromptScore(Base):
    __tablename__ = "prompt_score"

    prompt_score_id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_summary_id = Column(Integer, ForeignKey('assessment_area_summary.assessment_summary_id', ondelete='CASCADE'), nullable=False)
    prompt_id = Column(Integer, ForeignKey('prompt.prompt_id', ondelete='CASCADE'), nullable=False)
    prompt_score = Column(Float)
    max_score = Column(Integer)
    score_justification = Column(Text)
    reference = Column(Text)
    created_on = Column(TIMESTAMP, default=func.now())
    created_by = Column(String(100))