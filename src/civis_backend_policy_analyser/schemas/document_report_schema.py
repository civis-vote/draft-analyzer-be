from pydantic import Field
from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from typing import List, Optional
from datetime import datetime

from civis_backend_policy_analyser.schemas.executive_summary_schema import ExecutiveSummarySchema

class ReportSchema(BaseModelSchema):
    report_id: Optional[int] = None
    summary_id: int
    report_content: str
    created_on: Optional[datetime] = None
    created_by: str
    model_config = {
        "from_attributes": True
    }
    
class ReportResponseSchema(BaseModelSchema):
    report_id: Optional[int] = None
    summary_id: int
    report_content: str

    model_config = {
        "from_attributes": True
    }   

class ScoringItem(BaseModelSchema):
    criterion: str
    score: Optional[float] = None
    reasoning: Optional[str] = None
    reference: Optional[str] = None


class AssessmentArea(BaseModelSchema):
    area_number: int
    title: str
    explanation: str
    scoring_table: List[ScoringItem]
    summary: str


class CoverPageData(BaseModelSchema):
    report_title: str
    subtitle: str
    date: str
    submitted_to: str
    prepared_by: str
    executive_summary: str


class ReportRequest(BaseModelSchema):
    cover: CoverPageData
    assessments: List[AssessmentArea]