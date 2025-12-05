from pydantic import BaseModel, Field
from typing import Annotated


class Profile(BaseModel):
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


default_profile = Profile(
    **{
        "first_name": "first_name",
        "last_name": "last_name",
        "phone": "+71234567890",
    }
)
