from datetime import datetime

from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema


class ReportSchema(BaseModelSchema):
    report_id: int | None = None
    summary_id: int
    report_content: str
    created_on: datetime | None = None
    created_by: str
    model_config = {
        "from_attributes": True
    }
    
class ReportResponseSchema(BaseModelSchema):
    report_id: int | None = None
    summary_id: int
    report_content: str

    model_config = {
        "from_attributes": True
    }   

class ScoringItem(BaseModelSchema):
    criterion: str
    score: float | None = None
    reasoning: str | None = None
    reference: str | None = None


class AssessmentArea(BaseModelSchema):
    area_number: int
    title: str
    explanation: str
    scoring_table: list[ScoringItem]
    summary: str


class CoverPageData(BaseModelSchema):
    report_title: str
    subtitle: str
    date: str
    submitted_to: str
    prepared_by: str


class ReportRequest(BaseModelSchema):
    cover: CoverPageData
    assessments: list[AssessmentArea]