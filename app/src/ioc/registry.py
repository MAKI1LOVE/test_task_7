from collections.abc import Iterable

from dishka import Provider

from src.ioc.adapters import DBConnectionProvider, DBSessionProvider
from src.ioc.repositories import ArticleRepositoryProvider
from src.ioc.services import ParserProvider, ParserServiceProvider, ParserSettingsProvider
from src.ioc.settings import SettingsProvider
from src.ioc.utils import ParserClientProvider, ThreadPoolProvider


def get_service_providers() -> Iterable[Provider]:
    return (
        ParserProvider(),
        ParserServiceProvider(),
        ParserSettingsProvider(),
    )


def get_repository_providers() -> Iterable[Provider]:
    return (ArticleRepositoryProvider(),)


def get_util_providers() -> Iterable[Provider]:
    return (
        ThreadPoolProvider(),
        ParserClientProvider(),
    )


def get_adapters_providers() -> Iterable[Provider]:
    return (
        DBConnectionProvider(),
        DBSessionProvider(),
    )


def get_providers() -> Iterable[Provider]:
    return (
        SettingsProvider(),
        *get_adapters_providers(),
        *get_service_providers(),
        *get_repository_providers(),
        *get_util_providers(),
    )
