from fastapi import APIRouter, HTTPException
from civis_backend_policy_analyser.views.document_validate_view import DocumentValidateView
from civis_backend_policy_analyser.core.db_connection import DBSessionDep

validate_router = APIRouter(
    prefix='/api',
    tags=['validate'],
    responses={404: {'description': 'No document found.'}},
)

@validate_router.get(
    "document/{document_id}/validate",
    response_model=dict,
)
async def validate_document_(
    document_id: str,
    db_session: DBSessionDep,
):
    """
    Validate a document using LLM.
    """
    document_validate_service = DocumentValidateView(db_session)
    document_validate_response = await document_validate_service.validate_document(document_id)
    return document_validate_response