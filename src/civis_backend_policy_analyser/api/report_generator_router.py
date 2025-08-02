from fastapi import APIRouter

from civis_backend_policy_analyser.core.db_connection import DBSessionDep
from civis_backend_policy_analyser.schemas.document_summary_schema import DocumentReportOut
from civis_backend_policy_analyser.views.document_report_view import DocumentReportView

report_router = APIRouter(
    prefix='/api/report',
    tags=['report'],
    responses={404: {'description': 'Failed to generate report'}}
)

@report_router.get(
    "/{summary_id}",
    response_model=DocumentReportOut
)
async def generate_document_report(
    summary_id: int,
    db_session: DBSessionDep
):
    """
    Generate a report for the document belonging to the input summary_id
    """
    report_view = DocumentReportView(db_session)
    document_report = await report_view.generate_document_report(summary_id)
    return document_report
