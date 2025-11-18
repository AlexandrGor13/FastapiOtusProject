from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Annotated, Optional


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

    # @field_validator('phone')
    # @classmethod
    # def check_valid_phone(cls, phone: str):
    #     if not (phone[1:].isdigit() and phone[0] == '+'):
    #         raise ValueError('Неправильный ввод.')


class Profile(ProfileRead):
    user_id: Annotated[int, Field()]


default_profile = ProfileRead(
    **{
        "first_name": "first_name",
        "last_name": "last_name",
        "phone": "+71234567890",
    }
)
