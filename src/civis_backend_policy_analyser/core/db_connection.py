import contextlib
from collections.abc import AsyncIterator
from typing import Annotated
from sqlalchemy import event
import time
from civis_backend_policy_analyser.config.logging_config import logger

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
        # Add SQL logging events for async engine
        self._setup_event_listeners()

    def _setup_event_listeners(self):
        @event.listens_for(self._engine.sync_engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            context._query_start_time = time.perf_counter()
            logger.debug(f"Executing query: {statement}")
            logger.debug(f"Parameters: {parameters}")

        @event.listens_for(self._engine.sync_engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            total_time = time.perf_counter() - context._query_start_time
            logger.debug(f"Query completed in {total_time:.6f} seconds")

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