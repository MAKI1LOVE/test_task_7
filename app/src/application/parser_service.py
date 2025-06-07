from uuid import UUID

from src.application.base_article_repository import BaseArticleRepository
from src.domain.article import Article
from src.domain.base_parser_service import BaseParserService
from src.domain.base_url_parser import BaseUrlParser


class ParserService(BaseParserService):
    def __init__(self, parser_repository: BaseArticleRepository, url_parser: BaseUrlParser) -> None:
        self.repository = parser_repository
        self.url_parser = url_parser

    async def parse(self, url: str) -> Article | None:
        article = await self.url_parser.parse(url)
        if article is None:
            return None

        await self.save_parsed_article_with_siblings(article)
        return article

    async def save_parsed_article_with_siblings(self, article: Article) -> Article:
        articles_by_url = self.get_articles_by_url_dict(article)

        existing_articles = await self.repository.get_articles_by_url(articles_by_url.keys())
        for ea in existing_articles:
            articles_by_url[ea.url].id = ea.id

        articles_to_save = [a for a in articles_by_url.values() if a.id is None]
        if articles_to_save:
            new_articles = await self.repository.add_articles(articles_to_save)
            for new_article in new_articles:
                articles_by_url[new_article.url].id = new_article.id

        id_pairs = self.get_many_to_many_pairs(article)

        await self.repository.add_article_pairs(id_pairs)

        return article

    def get_articles_by_url_dict(self, article: Article) -> dict[str, Article]:
        articles_by_url = {article.url: article}

        def traverse_siblings(art: Article) -> None:
            for sibling in art.siblings:
                if sibling.url not in articles_by_url:
                    articles_by_url[sibling.url] = sibling
                    traverse_siblings(sibling)

        traverse_siblings(article)

        return articles_by_url

    def get_many_to_many_pairs(
        self,
        article: Article,
        m2m: set[tuple[UUID, UUID]] | None = None,
    ) -> set[tuple[UUID, UUID]]:
        if m2m is None:
            m2m: set[tuple[UUID, UUID]] = set()

        for sibling in article.siblings:
            pair = (article.id, sibling.id)
            if pair in m2m:
                continue

            m2m.add(pair)

        for sibling in article.siblings:
            pair = (article.id, sibling.id)
            if pair in m2m:
                continue
            m2m.union(self.get_many_to_many_pairs(sibling))

        return m2m
