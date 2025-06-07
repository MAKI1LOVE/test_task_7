from typing import Protocol

from src.domain.article import Article


class BaseUrlParser(Protocol):
    async def parse(self, url: str) -> Article | None:
        raise NotImplementedError
