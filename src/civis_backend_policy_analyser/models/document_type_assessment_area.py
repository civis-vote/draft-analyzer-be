from civis_backend_policy_analyser.models.base import Base
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Table, func, UniqueConstraint, Identity
from sqlalchemy.orm import relationship

DocumentTypeAssessmentArea = Table(
    'document_type_assessment_area',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('doc_type_id', Integer, ForeignKey('document_type.doc_type_id', ondelete='CASCADE')),
    Column('assessment_id', Integer, ForeignKey('assessment_area.assessment_id', ondelete='CASCADE')),
    Column('created_on', TIMESTAMP, default=func.now()),
    Column('updated_on', TIMESTAMP, default=func.now(), onupdate=func.now()),
    UniqueConstraint('doc_type_id', 'assessment_id', name='_doc_type_assessment_uc')
)

