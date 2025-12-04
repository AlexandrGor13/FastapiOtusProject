from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

from sqlalchemy import (
    MetaData,
    Integer,
    func,
    TIMESTAMP,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


async_engine = create_async_engine(
    url=settings.db.async_url,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    future=True,
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )

    @classmethod
    def get_columns(cls):
        lst_columns = [
            item
            for item in cls.__dict__.keys()
            if not (item[:2] == item[-2:] and item[:2] == "__")
            and not item.startswith("get")
            and not item.find("class") >= 0
        ]
        lst_columns.insert(0, lst_columns.pop(-3))
        return lst_columns
