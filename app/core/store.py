from redis import ConnectionError, Redis

from core.config import settings


class TokenDict:
    def __init__(self, host, port, db):
        self.host = host
        self.port = port
        self.db = db
        self.timeout = 3  # seconds
        self.connection = None

    def connect(self):
        """Создаем соединение с Redis"""
        try:
            connection = Redis(host=self.host, port=self.port, db=self.db, socket_timeout=self.timeout)
            connection.ping()  # проверяем доступность сервера
            self.connection = connection
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redis server: {e}")

    def add_token(self, token: str, username: str):
        self.connection.set(token, username)

    def del_token(self, token):
        self.connection.delete(token)

    def get_token(self, token):
        value = self.connection.get(token)
        return value.decode('utf-8') if value else None


token_dict = TokenDict(host=settings.redis.host, port=settings.redis.port, db=settings.redis.db)
token_dict.connect()