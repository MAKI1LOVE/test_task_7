from sqlalchemy import Column, ForeignKey, Index, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.base import Base, UUIDId

article_to_article = Table(
    'article_to_articles',
    Base.metadata,
    Column('parent_id', ForeignKey('article.id'), primary_key=True),
    Column('sibling_id', ForeignKey('article.id'), primary_key=True),
)


class Article(Base, UUIDId):
    __tablename__ = 'article'

    url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    parsed_text: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(String, nullable=False)
    siblings: Mapped[list['Article']] = relationship(
        'Article',
        secondary=article_to_article,
        primaryjoin='article_to_articles.c.parent_id==Article.id',
        secondaryjoin='article_to_articles.c.sibling_id==Article.id',
        backref='related_to',
    )


Index('article_url_idx', Article.url, postgresql_using='hash')
