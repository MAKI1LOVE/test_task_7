from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.connection import DBConnection
from src.settings import Settings


class DBConnectionProvider(Provider):
    @provide(scope=Scope.APP, provides=DBConnection)
    async def get_engine(self, settings: Settings) -> AsyncGenerator[DBConnection]:
        db_connection = DBConnection(settings.POSTGRES_SETTINGS)
        yield db_connection
        await db_connection.close()


class DBSessionProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def get_session(self, db_connection: DBConnection) -> AsyncGenerator[AsyncSession, None]:
        async with db_connection.get_async_sessionmaker()() as session:
            yield session
