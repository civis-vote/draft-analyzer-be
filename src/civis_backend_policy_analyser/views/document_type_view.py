from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from civis_backend_policy_analyser.models.assessment_area import AssessmentArea
from civis_backend_policy_analyser.models.document_type import DocumentType
from civis_backend_policy_analyser.schemas.document_type_schema import (
    DocumentTypeCreate,
    DocumentTypeOut,
    DocumentTypeUpdate,
)
from civis_backend_policy_analyser.views.base_view import BaseView


class DocumentTypeView(BaseView):
    """
    View controller to manage Document Types such as policy documents,
    consultation documents, legal drafts, etc.

    Business Rules:
    - Document types can be associated with multiple assessment areas.
    - The relationship is many-to-many and must be updated explicitly.
    """

    model = DocumentType
    schema = DocumentTypeOut

    async def all_document_types(self):
        """
        Fetch all document types along with their associated assessment areas.

        Returns:
            List[DocumentTypeOut]: Serialized document types with related assessment IDs.

        Business Logic:
        - Eagerly loads associated assessment areas to avoid async lazy-loading issues.
        """
        try:
            result = await self.db_session.execute(
                select(self.model).options(selectinload(self.model.assessment_areas))
            )
            all_records = result.scalars().all()
            return [self.schema.from_orm(record) for record in all_records]
        except Exception as e:
            logger.error(f"Failed to fetch document types: {e}")
            raise

    async def create(self, data: DocumentTypeCreate):
        """
        Create a new document type and associate it with selected assessment areas.

        Args:
            data (DocumentTypeCreate): Input data including assessment IDs.

        Returns:
            DocumentTypeOut: The created document type with associations.

        Business Logic:
        - Validates provided assessment area IDs.
        - Sets up many-to-many relationship manually before persisting.
        """
        try:
            assessment_ids = data.assessment_ids or []
            doc_data = data.model_dump(exclude={'assessment_ids'})
            model_obj = self.model(**doc_data)

            if assessment_ids:
                assessment_objs = (
                    await self.db_session.execute(
                        select(AssessmentArea).where(AssessmentArea.assessment_id.in_(assessment_ids))
                    )
                ).scalars().all()
                model_obj.assessment_areas = assessment_objs

            self.db_session.add(model_obj)
            await self.db_session.commit()
            await self.db_session.refresh(model_obj)

            return self.schema.from_orm(model_obj)
        except Exception as e:
            logger.error(f"Error creating DocumentType: {e}")
            raise

    async def update(self, id: int, data: DocumentTypeUpdate):
        """
        Update an existing document type and its associated assessment areas.

        Args:
            id (int): DocumentType ID to update.
            data (DocumentTypeUpdate): Fields to update.

        Returns:
            DocumentTypeOut: Updated document type with correct associations.

        Business Logic:
        - Partial updates are supported.
        - If assessment_ids are provided, the many-to-many relationship is replaced.
        """
        try:
            result = await self.db_session.execute(
                select(self.model)
                .options(selectinload(self.model.assessment_areas))
                .where(self.model.doc_type_id == id)
            )
            model_obj = result.scalars().first()

            if not model_obj:
                msg = f"DocumentType with id {id} not found."
                logger.warning(msg)
                raise ValueError(msg)

            update_data = data.model_dump(exclude_unset=True)
            assessment_ids = update_data.pop("assessment_ids", None)

            for key, value in update_data.items():
                setattr(model_obj, key, value)

            if assessment_ids is not None:
                result = await self.db_session.execute(
                    select(AssessmentArea).where(AssessmentArea.assessment_id.in_(assessment_ids))
                )
                assessment_objs = result.scalars().all()

                model_obj.assessment_areas.clear()
                model_obj.assessment_areas.extend(assessment_objs)

            await self.db_session.commit()
            await self.db_session.refresh(model_obj)

            return self.schema.from_orm(model_obj)

        except Exception as e:
            logger.error(f"Error updating DocumentType id={id}: {e}")
            raise
