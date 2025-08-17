from sqlalchemy import select
from sqlalchemy.orm import aliased
from loguru import logger

from civis_backend_policy_analyser.models.document_metadata import DocumentMetadata
from civis_backend_policy_analyser.models.document_summary import DocumentSummary
from civis_backend_policy_analyser.models.document_type import DocumentType
from civis_backend_policy_analyser.schemas.history_schema import DocumentHistorySchema, DocumentHistorySchemaOut
from civis_backend_policy_analyser.views.base_view import BaseView



class HistoryView(BaseView):
    schema = DocumentHistorySchema

    async def get_user_history(self, user_id: str) -> DocumentHistorySchemaOut:
        logger.info(f"Fetching history for user: {user_id}")

        ds = aliased(DocumentSummary)
        dt = aliased(DocumentType)
        dm = aliased(DocumentMetadata)

        query = (
            select(
                ds.doc_summary_id,
                ds.doc_type_id,
                ds.created_on.label("summary_time"),
                dt.doc_type_name.label("doc_type_name"),
                dm.file_name.label("file_name")
            )
            .join(dt, ds.doc_type_id == dt.doc_type_id)
            .join(dm, ds.doc_id == dm.doc_id)
            .where(ds.created_by == user_id)
            .order_by(ds.created_on.desc())
        )

        result = await self.db_session.execute(query)
        rows = result.mappings().all()

        # build history objects
        history = []
        for row in rows:
            history.append(
                DocumentHistorySchema(
                    doc_type_id=row["doc_type_id"],
                    doc_summary_id=row["doc_summary_id"],
                    file_name=row["file_name"],
                    summary_time=row["summary_time"],
                    status= "completed", # TODO update this once status is updated in table
                    doc_type=row["doc_type_name"]
                )
            )
        history_out = DocumentHistorySchemaOut(history=history)
        logger.info(f"User history fetched successfully: {history}")

        return history_out
