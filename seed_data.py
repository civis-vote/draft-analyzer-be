from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "postgresql+psycopg://ffg:ffg_jpmc_civis@localhost:5432/civis"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# -------------------
# ORM Models
# -------------------

class AssessmentArea(Base):
    __tablename__ = "assessment_area"
    assessment_id = Column(Integer, primary_key=True)
    assessment_name = Column(String(255), nullable=False)
    description = Column(Text)
    created_by = Column(String(100))
    created_on = Column(DateTime)
    updated_by = Column(String(100))
    updated_on = Column(DateTime)

class Prompt(Base):
    __tablename__ = "prompt"
    prompt_id = Column(Integer, primary_key=True)
    criteria = Column(String(255), nullable=False)
    question = Column(Text, nullable=False)
    created_by = Column(String(100))
    created_on = Column(DateTime)
    updated_by = Column(String(100))
    updated_on = Column(DateTime)

class AssessmentAreaPrompt(Base):
    __tablename__ = "assessment_area_prompt"
    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey("assessment_area.assessment_id", ondelete="CASCADE"))
    prompt_id = Column(Integer, ForeignKey("prompt.prompt_id", ondelete="CASCADE"))
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    __table_args__ = (UniqueConstraint('assessment_id', 'prompt_id', name='_assessment_prompt_uc'),)

class DocumentType(Base):
    __tablename__ = "document_type"
    doc_type_id = Column(Integer, primary_key=True)
    doc_type_name = Column(String(255), nullable=False)
    description = Column(Text)
    created_by = Column(String(100))
    created_on = Column(DateTime)
    updated_by = Column(String(100))
    updated_on = Column(DateTime)

class DocumentTypeAssessmentArea(Base):
    __tablename__ = "document_type_assessment_area"
    id = Column(Integer, primary_key=True)
    doc_type_id = Column(Integer, ForeignKey("document_type.doc_type_id", ondelete="CASCADE"))
    assessment_id = Column(Integer, ForeignKey("assessment_area.assessment_id", ondelete="CASCADE"))
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    __table_args__ = (UniqueConstraint('doc_type_id', 'assessment_id', name='_doc_type_assessment_uc'),)

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"
    doc_id = Column(String, primary_key=True)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    upload_time = Column(DateTime)
    number_of_pages = Column(Integer)
    doc_size_kb = Column(Integer)


def seed():
    session = SessionLocal()

    # Seed Assessment Areas
    assessment_areas = [
        AssessmentArea(assessment_id=1, assessment_name="Does the Draft Clearly Explain Why and What?", description="This area evaluates the depth and breadth of impact analysis in the policy document.", created_by="Admin", created_on=datetime(2025, 6, 16, 17, 35, 44), updated_on=datetime(2025, 6, 16, 17, 35, 44)),
        AssessmentArea(assessment_id=2, assessment_name="Does the Draft Thoroughly Assess the Impact?", description="This area evaluates the depth and breadth of impact analysis in the policy document.", created_by="Admin", created_on=datetime(2025, 6, 16, 17, 36, 54), updated_on=datetime(2025, 6, 21, 20, 20, 32)),
        AssessmentArea(assessment_id=3, assessment_name="Does the Draft Enable Meaningful Public Participation?", description="This area evaluates how well the policy enables and encourages public feedback and participation.", created_on=datetime(2025, 6, 21, 19, 48, 50), updated_on=datetime(2025, 6, 21, 19, 48, 50)),
    ]
    session.add_all(assessment_areas)
    session.commit()

    # Seed Prompts
    prompts = [
        Prompt(prompt_id=1, criteria="Justification", question="Is the need for the policy well-founded? Does the policy provide relevant context, data, or rationale for why it is needed?", created_by="Admin", created_on=datetime(2025, 6, 16, 17, 31, 18), updated_on=datetime(2025, 6, 16, 17, 31, 18)),
        Prompt(prompt_id=2, criteria="Essential Elements", question="Are the main objectives, provisions, or changes the policy introduces clearly stated? Does it specify what the policy aims to achieve?", created_by="Admin", created_on=datetime(2025, 6, 16, 17, 31, 59), updated_on=datetime(2025, 6, 16, 17, 31, 59)),
        Prompt(prompt_id=3, criteria="Comprehension", question="Is the policy text accessible, logically structured, and free of contradictions? Does it use clear language, headings, or summaries that aid understanding?", created_by="Admin", created_on=datetime(2025, 6, 16, 17, 32, 26), updated_on=datetime(2025, 6, 16, 17, 32, 26)),
        Prompt(prompt_id=4, criteria="Problem Identification", question="Does the policy define the root cause or specific issue it aims to address? Are challenges or market failures clearly outlined?", created_by="Admin", created_on=datetime(2025, 6, 16, 17, 32, 57), updated_on=datetime(2025, 6, 16, 17, 32, 57)),
        Prompt(prompt_id=5, criteria="Cost-Benefit Analysis", question="Does the policy include an economic or financial appraisal of its measures? Does it weigh potential benefits against costs or risks?", created_by="Admin", created_on=datetime(2025, 6, 16, 17, 33, 43), updated_on=datetime(2025, 6, 16, 17, 33, 43)),
        Prompt(prompt_id=6, criteria="Alternatives", question="Does the draft discuss other policy models or approaches? Is there a reason the chosen approach is deemed preferable?", created_by="Admin", created_on=datetime(2025, 6, 16, 17, 34, 12), updated_on=datetime(2025, 6, 16, 17, 34, 12)),
    ]
    session.add_all(prompts)
    session.commit()

    # Seed Assessment Area - Prompt mappings
    assessment_prompts = [
        AssessmentAreaPrompt(id=1, assessment_id=1, prompt_id=1, created_on=datetime(2025, 6, 16, 17, 35, 44), updated_on=datetime(2025, 6, 16, 17, 35, 44)),
        AssessmentAreaPrompt(id=2, assessment_id=1, prompt_id=2, created_on=datetime(2025, 6, 16, 17, 35, 44), updated_on=datetime(2025, 6, 16, 17, 35, 44)),
        AssessmentAreaPrompt(id=3, assessment_id=1, prompt_id=3, created_on=datetime(2025, 6, 16, 17, 35, 44), updated_on=datetime(2025, 6, 16, 17, 35, 44)),
        AssessmentAreaPrompt(id=4, assessment_id=2, prompt_id=4, created_on=datetime(2025, 6, 16, 17, 36, 54), updated_on=datetime(2025, 6, 16, 17, 36, 54)),
        AssessmentAreaPrompt(id=5, assessment_id=2, prompt_id=5, created_on=datetime(2025, 6, 16, 17, 36, 54), updated_on=datetime(2025, 6, 16, 17, 36, 54)),
        AssessmentAreaPrompt(id=6, assessment_id=2, prompt_id=6, created_on=datetime(2025, 6, 16, 17, 36, 54), updated_on=datetime(2025, 6, 16, 17, 36, 54)),
        AssessmentAreaPrompt(id=7, assessment_id=3, prompt_id=1, created_on=datetime(2025, 6, 21, 19, 48, 50), updated_on=datetime(2025, 6, 21, 19, 48, 50)),
        AssessmentAreaPrompt(id=8, assessment_id=3, prompt_id=2, created_on=datetime(2025, 6, 21, 19, 48, 50), updated_on=datetime(2025, 6, 21, 19, 48, 50)),
    ]
    session.add_all(assessment_prompts)
    session.commit()

    # Document Types
    doc_types = [
        DocumentType(doc_type_id=1, doc_type_name="Consultation", description="Documents related to public or internal consultations on policy matters. updated", created_by="admin_user", created_on=datetime(2025, 6, 16, 17, 40, 59), updated_on=datetime(2025, 6, 21, 20, 27, 55)),
        DocumentType(doc_type_id=2, doc_type_name="Law Order", description="Legal documents including new laws, orders, or government acts.", created_by="admin_user", created_on=datetime(2025, 6, 16, 17, 41, 17), updated_on=datetime(2025, 6, 16, 17, 41, 17)),
        DocumentType(doc_type_id=3, doc_type_name="Amendment", description="Documents describing proposed or enacted changes to existing laws or policies.", created_by="admin_user", created_on=datetime(2025, 6, 16, 17, 41, 34), updated_on=datetime(2025, 6, 16, 17, 41, 34)),
    ]
    session.add_all(doc_types)
    session.commit()

    # DocumentTypeAssessmentArea mappings
    dtaa = [
        DocumentTypeAssessmentArea(id=1, doc_type_id=1, assessment_id=1, created_on=datetime(2025, 6, 16, 17, 40, 59), updated_on=datetime(2025, 6, 16, 17, 40, 59)),
        DocumentTypeAssessmentArea(id=2, doc_type_id=1, assessment_id=2, created_on=datetime(2025, 6, 16, 17, 40, 59), updated_on=datetime(2025, 6, 16, 17, 40, 59)),
        DocumentTypeAssessmentArea(id=3, doc_type_id=2, assessment_id=1, created_on=datetime(2025, 6, 16, 17, 41, 17), updated_on=datetime(2025, 6, 16, 17, 41, 17)),
        DocumentTypeAssessmentArea(id=4, doc_type_id=3, assessment_id=2, created_on=datetime(2025, 6, 16, 17, 41, 34), updated_on=datetime(2025, 6, 16, 17, 41, 34)),
        DocumentTypeAssessmentArea(id=7, doc_type_id=1, assessment_id=3, created_on=datetime(2025, 6, 21, 20, 31, 50), updated_on=datetime(2025, 6, 21, 20, 31, 50)),
        DocumentTypeAssessmentArea(id=8, doc_type_id=3, assessment_id=3, created_on=datetime(2025, 6, 21, 20, 32, 18), updated_on=datetime(2025, 6, 21, 20, 32, 18)),
    ]
    session.add_all(dtaa)
    session.commit()

    # Document Metadata
    documents = [
        DocumentMetadata(doc_id="a0529cb6dc1e123d444db079d824b3e4cceeaff9c8e7abe4eca5b192f14d31d5", file_name="Electronic_Toys_Policy_14dot3 (1).pdf", file_type="application/pdf", upload_time=datetime(2025, 6, 16, 23, 13, 38), number_of_pages=26, doc_size_kb=951),
        DocumentMetadata(doc_id="36142d55edd7c4784f86b33ea20365430a1fcec64771006979d9ab95871adb2f", file_name="Odisha State Data Policy(OSDP)-2024_v07 (1)_0.pdf", file_type="application/pdf", upload_time=datetime(2025, 6, 22, 17, 12, 43), number_of_pages=39, doc_size_kb=1189),
        DocumentMetadata(doc_id="feee3807cadc5677d4fd630076e876a369253b1b39140f8caf6c256f370214bf", file_name="DRAFTDISCLOSURECLIMATERELATEDFINANCIALRISKS20249FBE3A566E7F487EBF9974642E6CCDB1 (1).pdf", file_type="application/pdf", upload_time=datetime(2025, 6, 22, 17, 14, 30), number_of_pages=12, doc_size_kb=568),
    ]
    session.add_all(documents)
    

    session.commit()
    print("Seeding completed.")
    session.close()

if __name__ == "__main__":
    seed()
