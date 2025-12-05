import pytest
from sqlalchemy.exc import NoResultFound
from app.core.schemas.user import User
from app.core.schemas.profile import Profile
from app.crud.user import UsersCRUD
from app.crud.profile import ProfileCRUD


@pytest.mark.asyncio
async def test_create_user(session):
    crud = UsersCRUD(session)
    new_user = User(
        username="test_user",
        email="test@example.com",
        password="password",
    )
    await crud.create(new_user)
    found_user = await crud.get_by_name(username="test_user")
    assert found_user.username == "test_user"
    assert found_user.email == "test@example.com"


@pytest.mark.asyncio
async def test_create_profile(session):
    crud = ProfileCRUD(session)
    new_profile = Profile(
        first_name="test_first_name",
        last_name="test_last_name",
        phone="+71111111111",
    )
    await crud.create("test_user", new_profile)
    found_profile = await crud.get_by_name(username="test_user")
    assert found_profile.first_name == "test_first_name"
    assert found_profile.last_name == "test_last_name"
    assert found_profile.phone == "+71111111111"


@pytest.mark.asyncio
async def test_update_user(session):
    crud = UsersCRUD(session)
    updated_user = User(
        username="new_test_user",
        email="new_test@example.com",
        password="new_password",
    )
    await crud.update("test_user", updated_user)
    updated_user = await crud.get_by_name(username="new_test_user")
    assert updated_user.username == "new_test_user"
    assert updated_user.email == "new_test@example.com"


@pytest.mark.asyncio
async def test_update_profile(session):
    crud = ProfileCRUD(session)
    updated_profile = Profile(
        first_name="new_test_first_name",
        last_name="new_test_last_name",
        phone="+72222222222",
    )
    await crud.update("new_test_user", updated_profile)
    updated_profile = await crud.get_by_name(username="new_test_user")
    assert updated_profile.first_name == "new_test_first_name"
    assert updated_profile.last_name == "new_test_last_name"
    assert updated_profile.phone == "+72222222222"


@pytest.mark.asyncio
async def test_delete_profile(session):
    crud = ProfileCRUD(session)
    await crud.delete("new_test_user")
    with pytest.raises(NoResultFound):
        await crud.get_by_name(username="new_test_user")


@pytest.mark.asyncio
async def test_delete_user(session):
    crud = UsersCRUD(session)
    new_user = User(
        username="test_user",
        email="test@example.com",
        password="password",
    )
    await crud.create(new_user)
    await crud.delete("test_user")
    with pytest.raises(NoResultFound):
        await crud.get_by_name(username="test_user")
