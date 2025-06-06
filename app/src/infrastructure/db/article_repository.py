from sqlalchemy import literal_column, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.base_article_repository import BaseArticleRepository
from src.domain.article import Article
from src.infrastructure.db.models import Article as ArticleModel
from src.infrastructure.db.models import article_to_article


class ArticleRepository(BaseArticleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_article(self, article: Article) -> Article:
        stmt = (
            insert(ArticleModel)
            .values(
                {
                    'url': article.url,
                    'summary': article.summary,
                    'parsed_text': article.parsed_text,
                },
            ).on_conflict_do_update()
            .returning(ArticleModel.id)
        )

        result = await self.session.execute(stmt)
        article.id = result.scalar_one()

        return article

    async def get_article(self, id: int) -> Article | None:
        stmt = select(ArticleModel).where(ArticleModel.id == id)
        result = (await self.session.execute(stmt)).scalar_one_or_none()

        if result is None:
            return None

        return Article(
            id=result.id,
            url=result.url,
            parsed_text=result.parsed_text,
            summary=result.summary,
        )

    async def get_article_with_siblings(self, id: int) -> Article | None:
        article = await self.get_article(id)
        if article is None:
            return None

        # TODO: change to with recursive
        a2a = article_to_article.alias('a2a')
        recursive_cte = (
            select(ArticleModel.id.label('sibling_id'), literal_column('1').label('depth'))
            .where(
                a2a.c.parent_id == id,
            )
            .cte(name='recursive_cte', recursive=True)
        )

        recursive_part = (
            select(
                a2a.c.sibling_id, (recursive_cte.c.depth + 1),
            ).join(recursive_cte, a2a.c.parent_id == recursive_cte.c.sibling_id).where(recursive_cte.c.depth < 5)
        )

        recursive_cte = recursive_cte.union_all(recursive_part)

        stmt = select(ArticleModel).join(recursive_cte, ArticleModel.id == recursive_cte.c.sibling_id).distinct()

        result = (await self.session.execute(stmt)).scalars().all()

        # TODO: change to object creation
        return article
