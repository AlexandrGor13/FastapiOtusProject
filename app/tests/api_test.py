from unittest.mock import patch
from app.crud.user import UsersCRUD
from app.core.security import get_password_hash


def test_create_user_success(test_app_mock_db, token_dict):
    """
    Создание нового пользователя
    """
    user_in = {
        "username": "new_user",
        "password": "password",
        "email": "new@user.com",
    }
    profile_in = {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "12345678",
    }
    token_dict.connect()
    response = test_app_mock_db.post(
        "/api/users",
        json={"user_in": user_in, "profile_in": profile_in},
    )
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["description"] == "User created"
    assert resp_json["user info"]["username"] == "new_user"
    assert resp_json["user info"]["email"] == "new@user.com"
    assert resp_json["profile"]["first_name"] == "John"
    assert resp_json["profile"]["last_name"] == "Doe"


def test_login_success(test_app_mock_db, token_dict):
    """
    Авторизация пользователя. В случае успеха возвращает токен доступа
    """
    token_dict.connect()
    item = {"username": "test_login_user", "password": "password", "role": "users"}
    item["password_hash"] = get_password_hash(item.pop("password"))
    with patch.object(
        UsersCRUD,
        "get_users_and_passwords",
        return_value=[item],
    ):
        response = test_app_mock_db.post(
            "/login",
            data={"username": "test_login_user", "password": "password"},
        )
        resp_json = response.json()
        assert response.status_code == 200
        assert "access_token" in resp_json
        assert "token_type" in resp_json
        assert resp_json["token_type"] == "bearer"
        assert len(resp_json["access_token"]) > 0


def test_protected_success(test_app_mock_db, new_token):
    """
    Проверка токена на доступ к ресурсу
    """
    token, item = new_token
    response = test_app_mock_db.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Access granted"}


def test_get_user_success(test_app_mock_db, new_token):
    """
    Получение данных пользователя
    """
    token, item = new_token
    with patch.object(
        UsersCRUD,
        "get_by_name",
        return_value={
            "username": item["username"],
            "email": item["email"],
        },
    ):
        response = test_app_mock_db.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        resp_json = response.json()
        assert resp_json["description"] == "User info"
        assert resp_json["user info"]["username"] == item["username"]
        assert resp_json["user info"]["email"] == item["email"]


def test_update_user_success(test_app_mock_db, new_token):
    """
    Обновление данных пользователя
    """
    user_in = {
        "username": "updated_user",
        "password": "updated_password",
        "email": "updated@user.com",
    }
    token, item = new_token
    with patch.object(
        UsersCRUD,
        "update",
        return_value={
            "username": user_in["username"],
            "email": user_in["email"],
        },
    ):
        response = test_app_mock_db.put(
            "/api/users/me",
            headers={"Authorization": f"Bearer {token}"},
            json=user_in,
        )
        assert response.status_code == 200
        resp_json = response.json()
        assert resp_json["description"] == "User updated"
        assert resp_json["user info"]["username"] == user_in["username"]
        assert resp_json["user info"]["email"] == user_in["email"]
