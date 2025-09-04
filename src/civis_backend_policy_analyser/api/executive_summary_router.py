from fastapi import APIRouter
from civis_backend_policy_analyser.config.logging_config import logger

from civis_backend_policy_analyser.core.db_connection import DBSessionDep
from civis_backend_policy_analyser.schemas.executive_summary_schema import ExecutiveSummarySchema
from civis_backend_policy_analyser.views.executive_summary_view import (
    ExecutiveSummaryView,
)

executive_summary_router = APIRouter(
    prefix='/api',
    tags=['executive_summary'],
    responses={404: {'description': 'No document found.'}},
)

@executive_summary_router.get(
    "/executive-summary/{doc_summary_id}",
    response_model=ExecutiveSummarySchema,
)
async def executive_summary_document(
    doc_summary_id: int,
    db_session: DBSessionDep,
):
    """
    Fetch document summary from llm.
    """
    try:
        document_summary_service = ExecutiveSummaryView(db_session)
        document_summary: ExecutiveSummarySchema = await document_summary_service.summarize_assessment_summaries(doc_summary_id)
        return document_summary
    except Exception as e:
        logger.error(f"Error fetching executive summary: {e}")
        raise