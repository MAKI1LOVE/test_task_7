from collections.abc import Iterable
from typing import Protocol
from uuid import UUID

from src.domain.article import Article


class BaseArticleRepository(Protocol):
    async def add_article(self, article: Article) -> Article:
        raise NotImplementedError

    async def add_articles(self, articles: Iterable[Article]) -> list[Article]:
        raise NotImplementedError

    async def get_article(self, id: UUID) -> Article | None:
        raise NotImplementedError

    async def get_article_with_siblings(self, id: UUID) -> Article | None:
        raise NotImplementedError

    async def get_articles_by_url(self, urls: Iterable[str]) -> list[Article]:
        raise NotImplementedError

    async def add_article_pairs(self, pairs: Iterable[tuple[UUID, UUID]]) -> None:
        raise NotImplementedError
