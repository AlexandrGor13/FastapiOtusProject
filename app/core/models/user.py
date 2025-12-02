from typing import TYPE_CHECKING
import enum
from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base
# from api.schemas.user import UserRead

if TYPE_CHECKING:
    from .profile import Profile

class RoleEnum(str, enum.Enum):
    admins = "admins"
    users = "users"

class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(15), unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(256), default=None)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    role: Mapped[RoleEnum] = mapped_column(default=RoleEnum.users)
    profile: Mapped["Profile"] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.username}"

    @property
    def get_schemas(self) -> dict[str, str]:
        return {
            "username": self.username,
            "email": self.email,
        }

    @property
    def get_username_password(self) -> dict:
        return {"username": self.username, "password_hash": self.password_hash, "role": self.role}


