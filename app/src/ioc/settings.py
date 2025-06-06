from dishka import Provider, Scope, from_context

from src.settings import Settings


class SettingsProvider(Provider):
    settings = from_context(scope=Scope.APP, provides=Settings)
