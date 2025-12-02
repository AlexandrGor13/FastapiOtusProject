from datetime import datetime, timedelta, timezone
from jose import jwt
import bcrypt
import secrets
from passlib.context import CryptContext
from core.config import settings

if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type("about", (object,), {"__version__": bcrypt.__version__}) # type: ignore[attr-defined]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_string(one_string: str, other_string: str) -> bool:
    """Функция для проверки, соответствует ли одна строка другой"""
    return secrets.compare_digest(one_string, other_string)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Функция для проверки, соответствует ли полученный пароль сохраненному хэшу"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """Функция генерации хэша пароля"""
    return pwd_context.hash(password)


def create_jwt_token(data: dict):
    """
    Функция для создания JWT токена.
    Мы копируем входные данные, добавляем время истечения и кодируем токен.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.token_timeout)
    payload.update({"exp": expire})
    return jwt.encode(claims=payload, key=settings.api.secret_key, algorithm="HS256")
