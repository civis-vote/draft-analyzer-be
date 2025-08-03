from datetime import datetime
from sqlalchemy import TIMESTAMP, Boolean, Float, create_engine, Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint, func
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
    assessment_id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_name = Column(String(255), nullable=False)
    description = Column(Text)
    summary_prompt = Column(Integer, nullable=False)
    created_by = Column(String(100))
    created_on = Column(DateTime)
    updated_by = Column(String(100))
    updated_on = Column(DateTime)

class Prompt(Base):
    __tablename__ = "prompt"
    prompt_type = Column(String(50), nullable=False)  # e.g., ASSESSMENT, VALIDATION
    prompt_id = Column(Integer, primary_key=True, autoincrement=True)
    criteria = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    technical_prompt = Column(Text, nullable=False)  # Detailed instructions for LLM
    created_by = Column(String(100))
    created_on = Column(DateTime)
    updated_by = Column(String(100))
    updated_on = Column(DateTime)

class AssessmentAreaPrompt(Base):
    __tablename__ = "assessment_area_prompt"
    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(Integer, ForeignKey("assessment_area.assessment_id", ondelete="CASCADE"))
    prompt_id = Column(Integer, ForeignKey("prompt.prompt_id", ondelete="CASCADE"))
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    __table_args__ = (UniqueConstraint('assessment_id', 'prompt_id', name='_assessment_prompt_uc'),)

class DocumentType(Base):
    __tablename__ = "document_type"
    doc_type_id = Column(Integer, primary_key=True, autoincrement=True)
    doc_type_name = Column(String(255), nullable=False)
    description = Column(Text)
    doc_validation_prompt = Column(Integer, nullable=False)  
    created_by = Column(String(100))
    created_on = Column(DateTime)
    updated_by = Column(String(100))
    updated_on = Column(DateTime)

class DocumentTypeAssessmentArea(Base):
    __tablename__ = "document_type_assessment_area"
    id = Column(Integer, primary_key=True, autoincrement=True)
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

class DocumentSummary(Base):
    __tablename__ = "document_summary"

    doc_summary_id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(String(100), ForeignKey('document_metadata.doc_id'), nullable=False)
    doc_type_id = Column(Integer, ForeignKey('document_type.doc_type_id'), nullable=False)

    is_valid_document = Column(Boolean, nullable=True)
    doc_valid_status_msg = Column(Text, nullable=True)

    summary_text = Column(Text, nullable=True)
    created_on = Column(TIMESTAMP, default=func.now())
    created_by = Column(String(100))


class AssessmentAreaSummary(Base):
    __tablename__ = "assessment_area_summary"

    assessment_summary_id = Column(Integer, primary_key=True, autoincrement=True)
    doc_summary_id = Column(Integer, ForeignKey('document_summary.doc_summary_id', ondelete='CASCADE'), nullable=False)
    assessment_id = Column(Integer, ForeignKey('assessment_area.assessment_id', ondelete='CASCADE'), nullable=False)
    summary_text = Column(Text)
    created_on = Column(TIMESTAMP, default=func.now())
    created_by = Column(String(100))

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

def seed():
    session = SessionLocal()

    # Seed Prompts
    prompts = [
        Prompt(prompt_type = "ASSESSMENT", criteria="Justification", description="Is the need for the policy well-founded? Does the policy provide relevant context, data, or rationale for why it is needed?", 
               technical_prompt = """You are evaluating the draft policy solely on the ‘Justification’ criterion. 
                    1) Carefully read every section of the draft. 
                    2) Identify and note why the policy says it is needed (problem statement, market gaps, legal obligations, statistics, context). 
                    3) In ≤ 40 words, summarise that rationale. 
                    4) Using the rubric below, assign a score 1‑5. 
                    5) Cite the exact section/page (or paragraph heading) that best supports your judgment. 
                    6) Return ONLY the JSON object described under ‘Expected JSON Output’. Do NOT add anything else.

                    Score 5 – Clear, data‑backed rationale with context & urgency  
                    4 – Strong rationale; minor evidence gaps  
                    3 – General claims; limited evidence  
                    2 – Vague need; little relevance  
                    1 – No discernible justification

                    json {
                    "criterion": "Justification",
                    "score": <1‑5>,
                    "reasoning": "<≤40 word summary>",
                    "ref": "<Section/page cited>"
                    }
                    """
                    ,
               created_by="Admin", created_on=datetime(2025, 6, 16, 17, 31, 18), updated_on=datetime(2025, 6, 16, 17, 31, 18)),
        Prompt(prompt_type = "ASSESSMENT", criteria="Essential Elements", description="Are the main objectives, provisions, or changes the policy introduces clearly stated? Does it specify what the policy aims to achieve?",
               technical_prompt="""
                            Evaluate ONLY the ‘Essential Elements’ criterion. 
                              1) Read the policy thoroughly. 
                              2) List for yourself (a) stated objectives, (b) scope (who/what is covered), (c) key measures/incentives. 
                              3) Judge if these are complete and explicit. 
                              4) In ≤ 40 words, summarise ‘what’ the policy proposes. 
                              5) Score 1‑5 with rubric. 
                              6) Cite the best supporting section/page. 
                              7) Output exactly the JSON object defined.

                              5 – Objectives, scope & measures are all explicit & detailed  
                              4 – Most elements clear; minor gaps  
                              3 – Some elements vague/missing  
                              2 – Major omissions or confusion  
                              1 – Very unclear or absent

                              json {
                                "criterion": "Essential Elements",
                                "score": <1‑5>,
                                "reasoning": "<≤40 word summary>",
                                "ref": "<Section/page cited>"
                              }
                """, 
                created_by="Admin", created_on=datetime(2025, 6, 16, 17, 31, 59), updated_on=datetime(2025, 6, 16, 17, 31, 59)),
        Prompt(prompt_type = "ASSESSMENT", criteria="Comprehension", description="Is the policy text accessible, logically structured, and free of contradictions? Does it use clear language, headings, or summaries that aid understanding?", 
               technical_prompt="""
               json {
                 "criterion": "Comprehension",
                 "score": <1‑5>,
                 "reasoning": "<≤40 word summary>",
                 "ref": "<Section/page cited>"
               }
               """,
               created_by="Admin", created_on=datetime(2025, 6, 16, 17, 32, 26), updated_on=datetime(2025, 6, 16, 17, 32, 26)),
        Prompt(prompt_type = "ASSESSMENT", criteria="Problem Identification", description="Does the policy define the root cause or specific issue it aims to address? Are challenges or market failures clearly outlined?", 
               technical_prompt="""
               json {
                 "criterion": "Comprehension",
                 "score": <1‑5>,
                 "reasoning": "<≤40 word summary>",
                 "ref": "<Section/page cited>"
               }
               """,
               created_by="Admin", created_on=datetime(2025, 6, 16, 17, 32, 57), updated_on=datetime(2025, 6, 16, 17, 32, 57)),
        Prompt(prompt_type = "ASSESSMENT", criteria="Cost-Benefit Analysis", description="Does the policy include an economic or financial appraisal of its measures? Does it weigh potential benefits against costs or risks?", 
               technical_prompt="""
               json {
                 "criterion": "Comprehension",
                 "score": <1‑5>,
                 "reasoning": "<≤40 word summary>",
                 "ref": "<Section/page cited>"
               }
               """,
               created_by="Admin", created_on=datetime(2025, 6, 16, 17, 33, 43), updated_on=datetime(2025, 6, 16, 17, 33, 43)),
        Prompt(prompt_type = "ASSESSMENT", criteria="Alternatives", description="Does the draft discuss other policy models or approaches? Is there a reason the chosen approach is deemed preferable?", 
               technical_prompt="""
               json {
                 "criterion": "Comprehension",
                 "score": <1‑5>,
                 "reasoning": "<≤40 word summary>",
                 "ref": "<Section/page cited>"
               }
               """,
               created_by="Admin", created_on=datetime(2025, 6, 16, 17, 34, 12), updated_on=datetime(2025, 6, 16, 17, 34, 12)),
        Prompt(prompt_type = "SUMMARY", criteria="Summary Prompt", description="",
               technical_prompt="""
                            You are a summarization assistant. Your task is to summarize documents concisely and professionally.
                            Instructions:
                            - Only include factual, useful information from the input.
                            - Do not include phrases like "Thinking...", "Let's see", or "As an AI".
                            - Do not explain your reasoning.
                            - Keep the summary objective and direct.
                            - return result in nice presentable html format
                            Now summarize the following content:
                """, 
                created_by="Admin", created_on=datetime(2025, 6, 16, 17, 31, 59), updated_on=datetime(2025, 6, 16, 17, 31, 59)),
        Prompt(prompt_type = "DOCUMENT_SUMMARY", criteria="Document Summary", description="Overall document summary", 
               technical_prompt="""
                You are a summarization assistant. Your task is to summarize documents concisely and professionally.
                Instructions:
                - Only include factual, useful information from the input.
                - Do not include phrases like "Thinking...", "Let's see", or "As an AI".
                - Do not explain your reasoning.
                - Keep the summary objective and direct.
                - return result in nice presentable html format
                Now summarize the following content:
               """,
               created_by="Admin", created_on=datetime(2025, 6, 16, 17, 34, 12), updated_on=datetime(2025, 6, 16, 17, 34, 12)),
        Prompt(prompt_type = "EXECUTIVE_SUMMARY", criteria="Executive Summary", description="Executive summary of analyzed document", 
               technical_prompt="""
                You are an executive summary assistant. Your task is to create an executive summary from the informations provided.
                The provided content is a detailed analysis of a document from various different aspects.
                Instructions:
                - Only include factual, useful information from the input.
                - Do not include phrases like "Thinking...", "Let's see", or "As an AI".
                - Do not explain your reasoning.
                - Keep the summary objective and direct.
                - return result in nice presentable html format
                - Executive summary has to be brief and should give the reader a good idea of the analysis carried out
                - Provide equal weightage to all the points provided in the content, do not put emphasis on just one aspect
                Now summarize the following content:
               """,
               created_by="Admin", created_on=datetime(2025, 6, 16, 17, 34, 12), updated_on=datetime(2025, 6, 16, 17, 34, 12)),
    ]
    session.add_all(prompts)
    session.commit()


    # Seed Assessment Areas
    assessment_areas = [
        AssessmentArea(assessment_name="Does the Draft Clearly Explain Why and What?", description="This area evaluates the depth and breadth of impact analysis in the policy document.", summary_prompt = 7, created_by="Admin", created_on=datetime(2025, 6, 16, 17, 35, 44), updated_on=datetime(2025, 6, 16, 17, 35, 44)),
        AssessmentArea(assessment_name="Does the Draft Thoroughly Assess the Impact?", description="This area evaluates the depth and breadth of impact analysis in the policy document.", summary_prompt = 7, created_by="Admin", created_on=datetime(2025, 6, 16, 17, 36, 54), updated_on=datetime(2025, 6, 21, 20, 20, 32)),
        AssessmentArea(assessment_name="Does the Draft Enable Meaningful Public Participation?", description="This area evaluates how well the policy enables and encourages public feedback and participation.", summary_prompt = 7, created_on=datetime(2025, 6, 21, 19, 48, 50), updated_on=datetime(2025, 6, 21, 19, 48, 50)),
    ]
    session.add_all(assessment_areas)
    session.commit()


    # Seed Assessment Area - Prompt mappings
    assessment_prompts = [
        AssessmentAreaPrompt(assessment_id=1, prompt_id=1, created_on=datetime(2025, 6, 16, 17, 35, 44), updated_on=datetime(2025, 6, 16, 17, 35, 44)),
        AssessmentAreaPrompt(assessment_id=1, prompt_id=2, created_on=datetime(2025, 6, 16, 17, 35, 44), updated_on=datetime(2025, 6, 16, 17, 35, 44)),
        AssessmentAreaPrompt(assessment_id=1, prompt_id=3, created_on=datetime(2025, 6, 16, 17, 35, 44), updated_on=datetime(2025, 6, 16, 17, 35, 44)),
        AssessmentAreaPrompt(assessment_id=2, prompt_id=4, created_on=datetime(2025, 6, 16, 17, 36, 54), updated_on=datetime(2025, 6, 16, 17, 36, 54)),
        AssessmentAreaPrompt(assessment_id=2, prompt_id=5, created_on=datetime(2025, 6, 16, 17, 36, 54), updated_on=datetime(2025, 6, 16, 17, 36, 54)),
        AssessmentAreaPrompt(assessment_id=2, prompt_id=6, created_on=datetime(2025, 6, 16, 17, 36, 54), updated_on=datetime(2025, 6, 16, 17, 36, 54)),
        AssessmentAreaPrompt(assessment_id=3, prompt_id=1, created_on=datetime(2025, 6, 21, 19, 48, 50), updated_on=datetime(2025, 6, 21, 19, 48, 50)),
        AssessmentAreaPrompt(assessment_id=3, prompt_id=2, created_on=datetime(2025, 6, 21, 19, 48, 50), updated_on=datetime(2025, 6, 21, 19, 48, 50)),
    ]
    session.add_all(assessment_prompts)
    session.commit()

    # Document Types
    doc_types = [
        DocumentType(doc_type_name="Consultation", description="Documents related to public or internal consultations on policy matters. updated", doc_validation_prompt = 1, created_by="admin_user", created_on=datetime(2025, 6, 16, 17, 40, 59), updated_on=datetime(2025, 6, 21, 20, 27, 55)),
        DocumentType(doc_type_name="Law Order", description="Legal documents including new laws, orders, or government acts.", doc_validation_prompt = 2, created_by="admin_user", created_on=datetime(2025, 6, 16, 17, 41, 17), updated_on=datetime(2025, 6, 16, 17, 41, 17)),
        DocumentType(doc_type_name="Amendment", description="Documents describing proposed or enacted changes to existing laws or policies.", doc_validation_prompt = 3, created_by="admin_user", created_on=datetime(2025, 6, 16, 17, 41, 34), updated_on=datetime(2025, 6, 16, 17, 41, 34)),
    ]
    session.add_all(doc_types)
    session.commit()

    # DocumentTypeAssessmentArea mappings
    dtaa = [
        DocumentTypeAssessmentArea(doc_type_id=1, assessment_id=1, created_on=datetime(2025, 6, 16, 17, 40, 59), updated_on=datetime(2025, 6, 16, 17, 40, 59)),
        DocumentTypeAssessmentArea(doc_type_id=1, assessment_id=2, created_on=datetime(2025, 6, 16, 17, 40, 59), updated_on=datetime(2025, 6, 16, 17, 40, 59)),
        DocumentTypeAssessmentArea(doc_type_id=2, assessment_id=1, created_on=datetime(2025, 6, 16, 17, 41, 17), updated_on=datetime(2025, 6, 16, 17, 41, 17)),
        DocumentTypeAssessmentArea(doc_type_id=3, assessment_id=2, created_on=datetime(2025, 6, 16, 17, 41, 34), updated_on=datetime(2025, 6, 16, 17, 41, 34)),
        DocumentTypeAssessmentArea(doc_type_id=1, assessment_id=3, created_on=datetime(2025, 6, 21, 20, 31, 50), updated_on=datetime(2025, 6, 21, 20, 31, 50)),
        DocumentTypeAssessmentArea(doc_type_id=3, assessment_id=3, created_on=datetime(2025, 6, 21, 20, 32, 18), updated_on=datetime(2025, 6, 21, 20, 32, 18)),
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
