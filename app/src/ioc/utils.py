from collections.abc import AsyncGenerator, Generator
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from aiohttp import ClientSession
from dishka import Provider, Scope, provide


class ThreadPoolProvider(Provider):
    @provide(provides=ThreadPoolExecutor, scope=Scope.APP)
    def thread_pool_provider(self) -> Generator[ThreadPoolExecutor, Any, None]:
        with ThreadPoolExecutor(max_workers=20) as executor:
            yield executor


class ParserClientProvider(Provider):
    @provide(provides=ClientSession, scope=Scope.APP)
    async def client_session_provider(self) -> AsyncGenerator[ClientSession, None]:
        async with ClientSession() as session:
            yield session
