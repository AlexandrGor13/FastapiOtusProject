from collections import namedtuple
from typing import Annotated
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import status, HTTPException, Form, Depends
from fastapi.security import OAuth2PasswordBearer
import logging

from app.core.models.user import RoleEnum
from app.core.schemas.user import UserAuth
from app.core.security import verify_password, verify_string
from app.core.config import settings
from app.core.store import token_dict
from app.crud.user import UsersCRUD, users_crud


log = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def auth_user_oath2(
    credentials: Annotated[UserAuth, Form()],
    crud: Annotated[UsersCRUD, Depends(users_crud)],
):
    """
    Функция для извлечения информации о пользователе из OAuth2PasswordBearer авторизации.
    Проверяем логин и пароль пользователя.
    """
    AuthData = namedtuple("AuthData", ["username", "password_hash", "role"])
    items = list(map(lambda us: AuthData(**us), await crud.get_users_and_passwords()))
    for item in items:
        is_user_ok = verify_string(credentials.username, item.username)
        is_pass_ok = verify_password(credentials.password, item.password_hash)
        if is_user_ok and is_pass_ok:
            return item
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(credentials: Annotated[str, Depends(oauth2_scheme)]):
    """Получение текущего пользователя из токена"""
    try:
        payload = jwt.decode(credentials, settings.api.secret_key)
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if username not in token_dict.get_user_by_token(credentials):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "role": role}
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_admin(dct: Annotated[dict, Depends(get_current_user)]):
    """Получение текущего пользователя из токена и проверка прав администратора"""
    if dct.get("role") != RoleEnum.admins:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return dct
