"""
Create
Read
Update
Delete
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.schemas.profile import Profile, default_profile
from app.core.models import Profile as ProfileModel, User as UserModel
from app.crud.base_crud import UsersItemsCRUD, get_async_session


class ProfileCRUD(UsersItemsCRUD):
    async def create(self, current_user: str, profile_in: Profile) -> Profile:
        params = profile_in.model_dump()
        user_id = await self.get_id_by_name(current_user)
        params["user_id"] = user_id
        profile = ProfileModel(**params)
        self.session.add(profile)
        profile_out = profile.get_schemas
        await self.session.commit()
        return Profile(**profile_out)

    async def update(self, current_user, profile_in: Profile) -> Profile:
        params = profile_in.model_dump()
        default_params = default_profile.model_dump()
        params = {k: w for k, w in params.items() if default_params[k] != w}
        user_id = await self.get_id_by_name(current_user)
        statement = (
            update(ProfileModel).where(ProfileModel.user_id == user_id).values(**params)
        )
        await self.session.execute(statement)
        await self.session.commit()
        profile_out = await self.get_by_name(current_user)
        return profile_out

    async def delete(self, current_user) -> Profile:
        statement = delete(UserModel).where(UserModel.username == current_user)
        profile_out = await self.get_by_name(current_user)
        await self.session.execute(statement)
        await self.session.commit()
        return profile_out

    async def get_by_name(self, username) -> Profile:
        statement = (
            select(ProfileModel).join(UserModel).where(UserModel.username == username)
        )
        profile_out = (await self.session.scalars(statement)).one().get_schemas
        return Profile(**profile_out)

    async def get(self) -> list:
        profile_list = []
        statement = select(ProfileModel).order_by(ProfileModel.id)
        profiles = await self.session.scalars(statement)
        for profile in profiles:
            profile_list.append(profile.get_schemas)
        return profile_list


def profile_crud(
    session: Annotated[
        AsyncSession,
        Depends(get_async_session),
    ],
) -> ProfileCRUD:
    return ProfileCRUD(session)
