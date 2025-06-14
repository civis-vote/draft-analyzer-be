from typing import Any

from loguru import logger
from sqlalchemy import select


class BaseView:
    """
    Base Controller view manages all common or generic action required to handle request-response services.

    Particularly it manages initialization of routine activities for each service and other generic functionality.
    """

    model: Any = None
    schema: Any = None

    def __init__(self, db_session):
        self.db_session = db_session
        self.select = select(self.model)

    async def all(self):
        try:
            # 1 Fetch all records from the defined SqlAlchemy Model.
            all_records = (await self.db_session.execute(self.select)).scalars().all()

            # 2 Validate and serialize each record using pydanctic model.
            all_records = [self.schema.from_orm(model_obj) for model_obj in all_records]

            return all_records
        except:
            logger.error(f'Error while fetch all records from table : {self.model}.')
            raise

    async def filter(self, **filter_kw_args):
        try:
            # 1 Select the records based on the filter fields given in query param.
            result = (
                (await self.db_session.execute(self.select.filter_by(**filter_kw_args)))
                .scalars()
                .all()
            )

            # 2 Validate and serialize each record using pydanctic model.
            filter_records = [self.schema.from_orm(model_obj) for model_obj in result]

            return filter_records
        except:
            logger.error(
                f'Error while fetch records by filter id: {filter_kw_args} from table : {self.model}.'
            )
            raise

    async def create(self, data):
        try:
            # 1 Create a new record in the database.
            if isinstance(data, self.model):
                model_obj = data
            else:
                model_obj = self.model(**data.dict())
            self.db_session.add(model_obj)
            await self.db_session.commit()
            await self.db_session.refresh(model_obj)

            # 2 Validate and serialize the created record using pydanctic model.
            created_record = self.schema.from_orm(model_obj)

            return created_record
        except Exception as e:
            logger.error(
                f'Error while creating record in table : {self.model}. Error: {e}'
            )
            raise

    async def update(self, id: int, data):
        try:
            # 1 Fetch the record to be updated.
            model_obj = await self.db_session.get(self.model, id)
            if not model_obj:
                raise ValueError(
                    f'Record with id {id} not found in table {self.model}.'
                )

            # 2 Update the record with new data.
            for key, value in data.dict().items():
                setattr(model_obj, key, value)

            await self.db_session.commit()
            await self.db_session.refresh(model_obj)

            # 3 Validate and serialize the updated record using pydanctic model.
            updated_record = self.schema.from_orm(model_obj)

            return updated_record
        except Exception as e:
            logger.error(
                f'Error while updating record with id {id} in table : {self.model}. Error: {e}'
            )
            raise

    async def delete(self, id: int):
        try:
            # 1 Fetch the record to be deleted.
            model_obj = await self.db_session.get(self.model, id)

            if not model_obj:
                raise ValueError(
                    f'Record with id {id} not found in table {self.model}.'
                )

            # 2 Delete the record from the database.
            await self.db_session.delete(model_obj)
            await self.db_session.commit()

            return {'message': f'Record with id {id} deleted successfully.'}
        except Exception as e:
            logger.error(
                f'Error while deleting record with id {id} in table : {self.model}. Error: {e}'
            )
            raise
