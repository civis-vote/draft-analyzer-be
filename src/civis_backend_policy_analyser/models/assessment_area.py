from sqlalchemy import Column, ForeignKey, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from civis_backend_policy_analyser.models.assessment_area_prompt import AssessmentAreaPrompt
from civis_backend_policy_analyser.models.base import Base
from civis_backend_policy_analyser.models.document_type_assessment_area import DocumentTypeAssessmentArea


class AssessmentArea(Base):
    __tablename__ = 'assessment_area'

    assessment_id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_name = Column(String(255), nullable=False)
    description = Column(Text)
    summary_prompt = Column(Integer, ForeignKey("prompt.prompt_id"), nullable=False) 
    created_by = Column(String(100))
    created_on = Column(TIMESTAMP, default=func.now())
    updated_by = Column(String(100))
    updated_on = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    document_types = relationship(
        "DocumentType",
        secondary=DocumentTypeAssessmentArea,
        back_populates="assessment_areas"
    )

    prompts = relationship( 
        "Prompt",
        secondary=AssessmentAreaPrompt.__table__, 
        back_populates="assessment_areas"
    )

    @property
    def prompt_ids(self) -> list[int]:
        # Return list of IDs only if relationship is loaded
        if 'prompts' not in self.__dict__:
            return []
        return [p.prompt_id for p in self.prompts]