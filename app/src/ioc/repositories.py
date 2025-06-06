from dishka import Provider, Scope, provide

from src.application.base_article_repository import BaseArticleRepository
from src.infrastructure.db.article_repository import ArticleRepository


class ArticleRepositoryProvider(Provider):
    article_repository = provide(ArticleRepository, scope=Scope.REQUEST , provides=BaseArticleRepository)
