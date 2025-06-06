from typing import Protocol

from src.domain.article import Article


class BaseUrlParser(Protocol):
    async def parse_url(self, url: str) -> Article:
        raise NotImplementedError
