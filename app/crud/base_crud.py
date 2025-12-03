"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from app.core.models.base import async_session
from app.core.models import User as UserModel


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session


class UsersItemsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_id_by_name(self, username: str) -> int:
        statement = select(UserModel.id).where(UserModel.username == username)
        return (await self.session.scalars(statement)).one()
