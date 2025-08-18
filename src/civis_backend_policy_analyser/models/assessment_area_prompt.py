from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)

from civis_backend_policy_analyser.models.base import Base


class AssessmentAreaPrompt(Base):
    __tablename__ = 'assessment_area_prompt'
    __table_args__ = (UniqueConstraint('assessment_id', 'prompt_id', name='_assessment_prompt_uc'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(Integer, ForeignKey('assessment_area.assessment_id', ondelete='CASCADE'), nullable=False)
    prompt_id = Column(Integer, ForeignKey('prompt.prompt_id', ondelete='CASCADE'), nullable=False)
    created_on = Column(TIMESTAMP, default=func.now())
    updated_on = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
