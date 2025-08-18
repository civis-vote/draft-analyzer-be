from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from civis_backend_policy_analyser.models.assessment_area import AssessmentArea
from civis_backend_policy_analyser.models.prompt import Prompt
from civis_backend_policy_analyser.schemas.assessment_area_schema import (
    AssessmentAreaCreate,
    AssessmentAreaOut,
    AssessmentAreaUpdate,
)
from civis_backend_policy_analyser.views.base_view import BaseView


class AssessmentAreaView(BaseView):
    """
    View controller to manage Assessment Areas, which are logical groupings used
    to categorize and evaluate different dimensions of a document or policy.

    Examples include:
    - Policy assessment area
    - Consultation assessment area
    - Legal compliance area

    Business Rules:
    - Each assessment area may be linked to multiple prompts (descriptions or criteria).
    - Prompts are managed via a many-to-many relationship.
    """

    model = AssessmentArea
    schema = AssessmentAreaOut

    async def all_assessment_areas(self):
        """
        Fetch all assessment areas with their related prompts eagerly loaded.

        Returns:
            List of AssessmentAreaOut schemas, each with associated prompt_ids.

        Business Logic:
        - Uses eager loading (`selectinload`) to pre-fetch prompts and avoid
          lazy-loading issues in async environments.
        """
        try:
            result = await self.db_session.execute(
                select(self.model).options(selectinload(self.model.prompts))
            )
            all_records = result.scalars().all()
            return [self.schema.from_orm(record) for record in all_records]
        except Exception as e:
            logger.error(f"Failed to fetch assessment areas: {e}")
            raise

    async def create(self, data: AssessmentAreaCreate):
        """
        Create a new assessment area and associate it with selected prompts.

        Args:
            data: AssessmentAreaCreate schema with optional prompt_ids.

        Returns:
            AssessmentAreaOut schema with prompt_ids populated.

        Business Logic:
        - Accepts a list of prompt IDs to associate.
        - Ensures referential integrity by querying Prompt model before assigning.
        """
        try:
            prompt_ids = data.prompt_ids or []
            area_data = data.model_dump(exclude={'prompt_ids'})
            model_obj = self.model(**area_data)

            if prompt_ids:
                prompt_objs = (
                    await self.db_session.execute(
                        select(Prompt).where(Prompt.prompt_id.in_(prompt_ids))
                    )
                ).scalars().all()
                model_obj.prompts = prompt_objs

            self.db_session.add(model_obj)
            await self.db_session.commit()
            await self.db_session.refresh(model_obj)

            return self.schema.from_orm(model_obj)

        except Exception as e:
            logger.error(f"Error creating AssessmentArea: {e}")
            raise

    async def update(self, id: int, data: AssessmentAreaUpdate):
        """
        Update an existing assessment area and its associated prompts.

        Args:
            id: ID of the assessment area to update.
            data: AssessmentAreaUpdate schema, may include updated prompt_ids.

        Returns:
            AssessmentAreaOut schema reflecting updated state.

        Business Logic:
        - Supports partial updates via `exclude_unset=True`.
        - If prompt_ids are provided, replaces existing associations.
        - Validates existence of related Prompt objects before linking.
        """
        try:
            result = await self.db_session.execute(
                select(self.model)
                .options(selectinload(self.model.prompts))
                .where(self.model.assessment_id == id)
            )
            model_obj = result.scalars().first()

            if not model_obj:
                msg = f"AssessmentArea with id {id} not found."
                logger.warning(msg)
                raise ValueError(msg)

            update_data = data.model_dump(exclude_unset=True)
            prompt_ids = update_data.pop("prompt_ids", None)

            for key, value in update_data.items():
                setattr(model_obj, key, value)

            if prompt_ids is not None:
                prompt_objs = (
                    await self.db_session.execute(
                        select(Prompt).where(Prompt.prompt_id.in_(prompt_ids))
                    )
                ).scalars().all()

                model_obj.prompts.clear()
                model_obj.prompts.extend(prompt_objs)

            await self.db_session.commit()
            await self.db_session.refresh(model_obj)

            return self.schema.from_orm(model_obj)

        except Exception as e:
            logger.error(f"Error updating AssessmentArea id={id}: {e}")
            raise
