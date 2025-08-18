from fastapi import APIRouter

from civis_backend_policy_analyser.core.db_connection import DBSessionDep
from civis_backend_policy_analyser.schemas.document_summary_schema import DocumentSummaryResponseSchema, DocumentSummarySchema
from civis_backend_policy_analyser.views.document_summary_view import DocumentSummaryView

summary_router = APIRouter(
    prefix='/api',
    tags=['summary'],
    responses={404: {'description': 'No summary found.'}},
)

@summary_router.get(
    "/summarize/{doc_summary_id}",
    response_model=DocumentSummaryResponseSchema,
)
async def summarize_document(
    doc_summary_id: int,
    db_session: DBSessionDep,
):
    """
    Fetch document summary from llm.
    """
    document_summary_service = DocumentSummaryView(db_session)
    document_summary = await document_summary_service.summarize_document(doc_summary_id)
    return document_summary


@summary_router.get(
    '/summary/{doc_summary_id}',
    response_model=DocumentSummarySchema,
)
async def get_document_existing_summary(
    doc_summary_id: int,
    db_session: DBSessionDep,
):
    """
    Get all document summaries in json format.
    """
    document_summary_service = DocumentSummaryView(db_session)
    document_summary = await document_summary_service.get(doc_summary_id)
    return document_summary


@summary_router.delete(
    "/summary/{doc_summary_id}",
    status_code=204,
)
async def delete_document_summary(
    doc_summary_id: int,
    db_session: DBSessionDep,
):
    """
    Delete a document summary.
    """
    document_summary_service = DocumentSummaryView(db_session)
    response = await document_summary_service.delete(doc_summary_id)
    return response
