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
