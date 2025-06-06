from collections.abc import Iterable, Sequence
from typing import Protocol

from src.domain.article import Article


class BaseArticleRepository(Protocol):
    async def save_article(self, article: Article) -> Article:
        raise NotImplementedError

    async def save_many_articles(self, articles: Iterable[Article]) -> list[Article]:
        raise NotImplementedError

    async def get_article(self, id: int) -> Article | None:
        raise NotImplementedError

    async def get_article_with_siblings(self, id: int) -> Article | None:
        raise NotImplementedError
