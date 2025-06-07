from uuid import UUID

from sqlalchemy import Integer, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class IntId:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class UUIDId:
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
