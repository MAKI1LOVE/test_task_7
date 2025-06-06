from collections.abc import Iterable

from dishka import Provider

from src.ioc.repositories import ArticleRepositoryProvider
from src.ioc.services import ParserProvider, ParserServiceProvider
from src.ioc.settings import SettingsProvider


def get_service_providers() -> Iterable[Provider]:
    return (
        ParserProvider(),
        ParserServiceProvider(),
    )

def get_repository_providers() -> Iterable[Provider]:
    return (
        ArticleRepositoryProvider(),
    )


def get_providers() -> Iterable[Provider]:
    return (
        SettingsProvider(),
        *get_service_providers(),
    )
