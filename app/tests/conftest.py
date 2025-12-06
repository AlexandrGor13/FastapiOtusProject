import unittest

import pytest
import pytest_asyncio
from unittest.mock import patch

from fastapi.testclient import TestClient
from fakeredis import FakeStrictRedis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.models.base import Base

DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="session")
async def engine():
    """Создаем асинхронный движок подключения к базе данных"""
    engine = create_async_engine(DB_URL, future=True)
    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    """Открываем новую сессию для каждого теста и автоматически закрываем её после завершения"""
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as sess:
        yield sess
        await sess.flush()
        await sess.rollback()


@pytest.fixture(scope="module")
def token_dict():
    """
    Создаем фикстуру для тестирования хранилища токенов
    """
    with patch("redis.Redis") as mock_redis:
        mock_redis.return_value = FakeStrictRedis()
        from app.core.store import TokenDict

        td = TokenDict(host="localhost", port=6379, db=0)
        return td


@pytest.fixture
def test_app_mock_db(session):
    """Создаем TestClient и моделируем базу данных."""
    from app.main import app
    from app.crud.base_crud import get_async_session

    app.dependency_overrides[get_async_session] = lambda: unittest.mock.MagicMock(
        session
    )
    with TestClient(app) as client:
        yield client

    # remove the mock at the end of the test
    del app.dependency_overrides[get_async_session]
