from unittest.mock import patch
from fastapi.encoders import jsonable_encoder
from app.core.schemas import User, Profile
from app.crud.user import UsersCRUD
from app.core.security import get_password_hash, create_jwt_token


def test_create_user_success(test_app_mock_db, token_dict):
    """
    Создание нового пользователя
    """
    user_in = User(username="new_user", email="new@user.com", password="password")
    profile_in = Profile(first_name="John", last_name="Doe", phone="12345678")
    token_dict.connect()
    response = test_app_mock_db.post(
        "/api/users",
        json=jsonable_encoder(
            {"user_in": user_in.model_dump(), "profile_in": profile_in.model_dump()}
        ),
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


def test_protected_success(test_app_mock_db, token_dict):
    """
    Проверка токена на доступ к ресурсу
    """
    token_dict.connect()
    item = {"username": "test_login_user", "password": "password", "role": "users"}
    item["password_hash"] = get_password_hash(item.pop("password"))
    token = create_jwt_token({"sub": item.get("username"), "role": item.get("role")})
    token_dict.add_token(token=token, username=item.get("username"))
    response = test_app_mock_db.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Access granted"}
