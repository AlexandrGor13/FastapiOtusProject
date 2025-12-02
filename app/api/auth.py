from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
import logging
from core.schemas.user import UserAuth
from core.schemas.token import Token
from core.security import create_jwt_token
from dependencies.dependencies import auth_user_oath2, oauth2_scheme, token_dict

router = APIRouter(tags=["Authentification"])
log = logging.getLogger(__name__)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="User authentification",
    responses={
        status.HTTP_200_OK: {
            "description": "User login",
            "content": {
                "application/json": {
                    "example": {"access_token": "token", "token_type": "bearer"}
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        },
    },
)
def login(
    user_in: Annotated[UserAuth, Depends(auth_user_oath2)],
) -> Token:
    """
    Авторизация пользователя. В случае успеха возвращает токен доступа
    """
    token = create_jwt_token({"sub": user_in.username, "role": user_in.role})
    token_dict.add_token(token=token, username=user_in.username)
    log.info("Login username %s", user_in.username)
    return Token(access_token=token, token_type="bearer")


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="User authentification",
    responses={
        status.HTTP_200_OK: {
            "description": "User logout",
            "content": {
                "application/json": {
                    "example": {"access_token": "token", "token_type": "bearer"}
                }
            },
        },
    },
)
def logout(token: str = Depends(oauth2_scheme)):
    """
    Выход из авторизации.
    """
    username = token_dict.del_token(token)
    log.info("Logout username %s", username)
    return {"msg": "Successfully logged out"}


@router.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    """
    Проверка токена на доступ к ресурсу.
    """
    if not token_dict.get_token(token):
        raise HTTPException(status_code=403, detail="Token has been blacklisted")
    return {"msg": "Access granted"}
