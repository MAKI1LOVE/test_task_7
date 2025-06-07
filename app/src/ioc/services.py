from dishka import Provider, Scope, provide

from src.application.parser_service import ParserService
from src.application.parsers.wiki_parser import ParserSettings, WikiParser
from src.domain.base_parser_service import BaseParserService
from src.domain.base_url_parser import BaseUrlParser
from src.settings import Settings


class ParserServiceProvider(Provider):
    parser_service = provide(ParserService, scope=Scope.REQUEST, provides=BaseParserService)

class ParserProvider(Provider):
    parser = provide(WikiParser, scope=Scope.REQUEST, provides=BaseUrlParser)

class ParserSettingsProvider(Provider):
    @provide(provides=ParserSettings, scope=Scope.APP)
    def get_parser_settings(self, settings: Settings) -> ParserSettings:
        return ParserSettings(NESTING=settings.NESTING)
