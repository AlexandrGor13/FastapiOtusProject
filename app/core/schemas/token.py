from pydantic import BaseModel

class Token(BaseModel):
    """Модель, используемая для ответа токеном при авторизации"""
    access_token: str
    token_type: str