import contextlib
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from civis_backend_policy_analyser.utils.constants import POSTGRES_CONNECTION_STRING


class DatabaseSessionManager:
    def __init__(self):
        engine_keywords = {}
        self._engine = create_async_engine(POSTGRES_CONNECTION_STRING, **engine_keywords)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception('DatabaseSessionManager is not initialized')
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception('DatabaseSessionManager is not initialized')

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception('DatabaseSessionManager is not initialized')

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager()


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
