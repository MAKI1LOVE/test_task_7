from src.application.base_article_repository import BaseArticleRepository
from src.domain.article import Article
from src.domain.base_parser_service import BaseParserService
from src.domain.base_url_parser import BaseUrlParser


class ParserService(BaseParserService):
    def __init__(self, parser_repository: BaseArticleRepository, url_parser: BaseUrlParser) -> None:
        self.repository = parser_repository
        self.url_parser = url_parser

    async def parse(self, url: str) -> Article:
        article = await self.url_parser.parse_url(url)
        await self.repository.save_article(article)
        return article

    async def save_parsed_article_with_siblings(self, article: Article) -> Article:
        articles_by_url = {article.url: article}

        def traverse_siblings(art: Article) -> None:
            for sibling in art.siblings:
                if sibling.url not in articles_by_url:
                    articles_by_url[sibling.url] = sibling
                    traverse_siblings(sibling)

        traverse_siblings(article)

        articles_to_save = articles_by_url.values()
        new_articles = await self.repository.save_many_articles(articles_to_save)

        for new_article in new_articles:
            articles_by_url[new_article.url].id = new_article.id

        return article
