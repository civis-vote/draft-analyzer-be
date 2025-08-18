from fastapi import APIRouter, File, HTTPException, UploadFile

from civis_backend_policy_analyser.core.db_connection import DBSessionDep
from civis_backend_policy_analyser.schemas.document_metadata_schema import (
    DocumentMetadataBase,
    DocumentMetadataOut,
)
from civis_backend_policy_analyser.views.document_metadata_view import (
    DocumentMetadataView,
)

document_router = APIRouter(
    prefix='/api',
    tags=['upload_policy'],
    responses={404: {'description': 'Invalid upload or file not found.'}},
)

@document_router.post("/upload_policy", response_model=DocumentMetadataOut)
async def upload_document(
    db_session: DBSessionDep,
    file: UploadFile = File(...),
):
    view = DocumentMetadataView(db_session)
    try:
        return await view.upload_policy_document(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@document_router.post(
    '/create_document',
    response_model=DocumentMetadataOut,
    status_code=201,
)
async def create_document(
    document: DocumentMetadataBase,
    db_session: DBSessionDep,
):
    """
    Create a new document entry.
    """
    document_service = DocumentMetadataView(db_session)
    created_document = await document_service.create(document)
    return created_document
