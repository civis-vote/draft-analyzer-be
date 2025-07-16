from fastapi import APIRouter

from civis_backend_policy_analyser.core.db_connection import DBSessionDep
from civis_backend_policy_analyser.schemas.document_score_schema import DocumentScoreOut
from civis_backend_policy_analyser.views.dcoument_score_view import DocumentScoreView

score_router = APIRouter(
    prefix='/api',
    tags=['score'],
    responses={404: {'description': 'Failed to assess document'}}
)

@score_router.get(
    "/document/{document_id}/assessment/{assessment_id}",
    response_model=DocumentScoreOut
)
async def score_assessment_area(
    document_id: str,
    assessment_id: int,
    db_session: DBSessionDep
):
    """
    Score the assessment belonging to the input assessment_id
    """
    scoring_view = DocumentScoreView(db_session)
    assessment_score = await scoring_view.score_assessment_area(document_id, assessment_id)
    return assessment_score
