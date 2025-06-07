from collections.abc import AsyncGenerator, Iterable
from contextlib import asynccontextmanager
from typing import Any

from dishka import AsyncContainer, Provider, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.ioc.registry import get_providers
from src.settings import Settings


def app_factory() -> FastAPI:
    app = create_app()
    configure_app(app)

    async_container = create_async_container(providers=(*get_providers(),))
    setup_dishka(container=async_container, app=app)

    return app


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    yield
    app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    return app


def configure_app(app: FastAPI) -> None:
    from src.presentation.root_router import router

    app.include_router(router)


def create_async_container(providers: Iterable[Provider]) -> AsyncContainer:
    settings = Settings()
    return make_async_container(*providers, context={Settings: settings})
