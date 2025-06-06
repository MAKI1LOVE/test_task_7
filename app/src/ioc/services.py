from dishka import Provider, Scope, provide

from src.application.parser_service import ParserService
from src.application.parsers.wiki_parser import WikiParser
from src.domain.base_parser_service import BaseParserService
from src.domain.base_url_parser import BaseUrlParser


class ParserServiceProvider(Provider):
    parser_service = provide(ParserService, scope=Scope.REQUEST, provides=BaseParserService)

class ParserProvider(Provider):
    parser = provide(WikiParser, scope=Scope.REQUEST, provides=BaseUrlParser)
