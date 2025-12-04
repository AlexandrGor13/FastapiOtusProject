import pytest
from unittest.mock import patch
from fakeredis import FakeStrictRedis


# @patch("redis.Redis", new_callable=lambda: FakeStrictRedis)
@pytest.fixture(scope="module")
def token_dict():
    with patch("redis.Redis") as mock_redis:
        mock_redis.return_value = FakeStrictRedis()
        from app.core.store import TokenDict

        td = TokenDict(host="localhost", port=6379, db=0)
        return td


def test_token_dict_connect(token_dict):
    token_dict.connect()
    assert token_dict.connection is not None


def test_token_dict_add_and_get(token_dict):
    token_dict.connect()
    # Добавляем токен
    token = "sample-token"
    username = "test-user"
    token_dict.add_token(token, username)

    # Проверяем сохранение токена
    retrieved_token = token_dict.get_user_by_token(token)
    assert retrieved_token == username


def test_token_dict_delete(token_dict):
    token_dict.connect()
    # Добавляем токен
    token = "another-sample-token"
    username = "another-test-user"
    token_dict.add_token(token, username)

    # Удаляем токен
    token_dict.del_token(token)

    # Проверяем удаление
    deleted_username = token_dict.get_user_by_token(token)
    assert deleted_username is None
