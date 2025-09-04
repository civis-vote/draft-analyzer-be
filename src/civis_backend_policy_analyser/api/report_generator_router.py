from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from civis_backend_policy_analyser.config.logging_config import logger

from civis_backend_policy_analyser.core.db_connection import DBSessionDep
from civis_backend_policy_analyser.schemas.document_summary_schema import DocumentReportOut
from civis_backend_policy_analyser.views.document_report_view import DocumentReportView

report_router = APIRouter(
    prefix='/api/report',
    tags=['report'],
    responses={404: {'description': 'Failed to generate report'}}
)

@report_router.get(
    "/generate/{doc_summary_id}",
    response_model=DocumentReportOut
)
async def generate_document_report(
    doc_summary_id: int,
    db_session: DBSessionDep
):
    """
    Generate a report for the document belonging to the input doc_summary_id
    """
    report_view = DocumentReportView(db_session)
    document_report = await report_view.generate_document_report(doc_summary_id)
    return document_report

@report_router.get(
    "/download/{doc_summary_id}",
    response_class=FileResponse
)
async def download_report(doc_summary_id: int, db_session: DBSessionDep) -> FileResponse:
    try:
        report_view = DocumentReportView(db_session)

        download_report: FileResponse = await report_view.download_report(doc_summary_id)
        return download_report
    
    except Exception as e:
        logger.error(f"Error downloading report for doc_summary_id {doc_summary_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to download report: {str(e)}")