from fastapi import APIRouter

from civis_backend_policy_analyser.core.db_connection import DBSessionDep
from civis_backend_policy_analyser.schemas.document_summary_schema import (
    DocumentSummaryBaseSchema,
)
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
    response_model=DocumentSummaryBaseSchema,
)
async def executive_summary_document(
    doc_summary_id: int,
    db_session: DBSessionDep,
):
    """
    Fetch document summary from llm.
    """
    document_summary_service = ExecutiveSummaryView(db_session)
    document_summary = await document_summary_service.executive_summary_document(doc_summary_id)
    return document_summary