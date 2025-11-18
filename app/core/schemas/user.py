from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional


class UserRead(BaseModel):
    username: Annotated[
        str,
        Field(
            min_length=3,
            max_length=15,
            description="Логин пользователя, от 3 до 15 символов",
        ),
    ]
    email: Annotated[EmailStr, Field(description="Электронная почта пользователя")]


class User(UserRead):
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=20,
            description="Пароль пользователя, от 8 до 20 символов",
        ),
    ]


class UserAuth(BaseModel):
    username: Annotated[str, Field()]
    password: Annotated[str, Field()]
    # password_hash: Annotated[str, Field()]


default_user = User(
    **{
        "username": "user",
        "email": "user@example.com",
        "password": "password",
    }
)
