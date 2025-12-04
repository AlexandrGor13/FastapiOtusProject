import pytest
from sqlalchemy.exc import NoResultFound
from app.core.schemas.user import User
from app.crud.user import UsersCRUD


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
async def test_delete_user(session):
    crud = UsersCRUD(session)
    await crud.delete("new_test_user")
    with pytest.raises(NoResultFound):
        await crud.get_by_name(username="new_test_user")
