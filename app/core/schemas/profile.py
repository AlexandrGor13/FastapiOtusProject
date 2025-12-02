from pydantic import BaseModel, Field
from typing import Annotated


class ProfileRead(BaseModel):
    first_name: Annotated[
        str, Field(max_length=30, description="Имя пользователя, до 50 символов")
    ] = ""
    last_name: Annotated[
        str, Field(max_length=30, description="Фамилия пользователя, до 50 символов")
    ] = ""
    phone: Annotated[
        str,
        Field(
            min_length=5,
            max_length=15,
            description="Номер телефона в международном формате, начинающийся с '+'",
        ),
    ]


class Profile(ProfileRead):
    user_id: Annotated[int, Field()]


default_profile = ProfileRead(
    **{
        "first_name": "first_name",
        "last_name": "last_name",
        "phone": "+71234567890",
    }
)
