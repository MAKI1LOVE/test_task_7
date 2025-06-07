from abc import abstractmethod
from typing import Protocol

from src.domain.article import Article


class BaseParserService(Protocol):
    @abstractmethod
    async def parse(self, url: str) -> Article | None:
        raise NotImplementedError
