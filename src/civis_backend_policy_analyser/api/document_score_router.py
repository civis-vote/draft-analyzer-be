from typing import List
from fastapi import APIRouter

from civis_backend_policy_analyser.core.db_connection import DBSessionDep
from civis_backend_policy_analyser.schemas.assessment_area_summary_schema import AssessmentAreaSummaryOut, AssessmentAreaSummarySchema
from civis_backend_policy_analyser.schemas.prompt_score_schema import PromptScoreSchema
from civis_backend_policy_analyser.views.prompt_score_view import PromptScoreView
from civis_backend_policy_analyser.views.assessment_area_summary_view import AssessmentAreaSummaryView

score_router = APIRouter(
    prefix='/api',
    tags=['score'],
    responses={404: {'description': 'Failed to assess document'}}
)

@score_router.get(
    "/summary/{doc_summary_id}/assessment/{assessment_id}",
    response_model=AssessmentAreaSummaryOut
)
async def score_assessment_area(
    doc_summary_id: int,
    assessment_id: int,
    db_session: DBSessionDep
):
    """
    Score the assessment belonging to the input assessment_id
    """
    summary_view : AssessmentAreaSummaryView = AssessmentAreaSummaryView(db_session)
    scoring_view : PromptScoreView = PromptScoreView(db_session)
    assessment_area_summary: AssessmentAreaSummarySchema = await summary_view.summarize_assessment_area(doc_summary_id, assessment_id)
    assessment_scores: List[PromptScoreSchema] = await scoring_view.score_assessment_area(assessment_area_summary)
    assessment_area_analysis: AssessmentAreaSummaryOut = await summary_view.format_result(assessment_area_summary, assessment_scores)
    return assessment_area_analysis
