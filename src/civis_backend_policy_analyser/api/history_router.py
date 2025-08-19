from fastapi import APIRouter
from loguru import logger

from civis_backend_policy_analyser.core.db_connection import DBSessionDep
from civis_backend_policy_analyser.schemas.history_schema import DocumentHistorySchemaOut
from civis_backend_policy_analyser.views.history_view import HistoryView


history_router = APIRouter(
    prefix='/api/history',
    tags=['history'],
    responses={404: {'description': 'No history found.'}},
)


@history_router.get('/{user_id}')
async def get_history_report(user_id: str, db_session: DBSessionDep) -> DocumentHistorySchemaOut:
    """
    Fetch the history report for the given user_id.
    """
    try:
        history_view = HistoryView(db_session)
        history = await history_view.get_user_history(user_id)
        return history
    except Exception as e:
        logger.error(f"Error fetching history for user {user_id}: {e}")
        return {"message": f"History report for user {user_id} not available yet."}