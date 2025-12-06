from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
import logging
from app.core.schemas.token import Token
from app.core.security import create_jwt_token
from app.dependencies.dependencies import auth_user_oath2, oauth2_scheme, token_dict

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
    user_in: Annotated[dict, Depends(auth_user_oath2)],
) -> Token:
    """
    Авторизация пользователя. В случае успеха возвращает токен доступа
    """
    token = create_jwt_token(
        {"sub": user_in.get("username"), "role": user_in.get("role")}
    )
    token_dict.add_token(token=token, username=str(user_in.get("username")))
    log.info("Login username %s", user_in.get("username"))
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
    if not token_dict.get_user_by_token(token):
        raise HTTPException(status_code=403, detail="Token has been blacklisted")
    return {"msg": "Access granted"}
