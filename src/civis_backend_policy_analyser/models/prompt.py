from sqlalchemy import TIMESTAMP, Column, Integer, String, Text, func
from sqlalchemy.orm import relationship

from civis_backend_policy_analyser.models.assessment_area_prompt import (
    AssessmentAreaPrompt,
)
from civis_backend_policy_analyser.models.base import Base


class Prompt(Base):
    __tablename__ = 'prompt'

    prompt_id = Column(Integer, primary_key=True, autoincrement=True)
    prompt_type = Column(String(50), nullable=False)
    criteria = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    technical_prompt = Column(Text, nullable=False)
    created_by = Column(String(100))
    created_on = Column(TIMESTAMP, default=func.now())
    updated_by = Column(String(100))
    updated_on = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    assessment_areas = relationship(
        "AssessmentArea",
        secondary=AssessmentAreaPrompt.__table__,
        back_populates="prompts"
    )