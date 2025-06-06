from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.settings import PostgresSettings


class DBConnection:
    def __init__(self, db_settings: PostgresSettings) -> None:
        self._engine = create_async_engine(db_settings.url)
        self._async_session_maker = async_sessionmaker(self._engine, class_=AsyncSession)

    async def close(self) -> None:
        await self._engine.dispose()

    def get_async_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        return self._async_session_maker
