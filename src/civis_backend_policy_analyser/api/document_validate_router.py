from fastapi import APIRouter, HTTPException
from civis_backend_policy_analyser.schemas.document_summary_schema import DocumentSummaryBaseSchema
from civis_backend_policy_analyser.views.document_validate_view import DocumentValidateView
from civis_backend_policy_analyser.core.db_connection import DBSessionDep

validate_router = APIRouter(
    prefix='/api',
    tags=['validate'],
    responses={404: {'description': 'No document found.'}},
)

@validate_router.get(
    "/document/{doc_id}/document-type/{doc_type_id}/validate",
    response_model=DocumentSummaryBaseSchema,
)
async def validate_document_(
    doc_id: str,
    doc_type_id: int,
    db_session: DBSessionDep,
):
    """
    Validate a document using LLM.
    """
    document_validate_service = DocumentValidateView(db_session)
    document_validate_response = await document_validate_service.validate_document(doc_id, doc_type_id)
    return document_validate_response