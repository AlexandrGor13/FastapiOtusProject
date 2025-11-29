from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent

SQLA_PG_ASYNC_ENGINE = "asyncpg"

class RedisConfig(BaseModel):
    """
    Setting for Redis
    """
    db: int = 0
    host: str
    port: int = 6379

class ApiConfig(BaseModel):
    """
    Setting for the API
    """
    secret_key: str
    kandinsky_host: str
    kandinsky_port: int = 8001
    deepface_host: str
    deepface_port: int = 8002

class AdminConfig(BaseModel):
    """
    Setting for the AdminPanel
    """
    user: str
    password: str


class DatabaseConfig(BaseModel):
    """
    Setting for the PostgreSQL database
    """
    name: str
    user: str
    password: str
    host: str
    port: int = 5432

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 0

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    def create_pg_url(self, engine: str) -> str:
        dsn = PostgresDsn(
            f"postgresql+{engine}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )
        return dsn.encoded_string()

    @property
    def async_url(self) -> str:
        return self.create_pg_url(SQLA_PG_ASYNC_ENGINE)


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file=(
            BASE_DIR / ".env.redis",
            BASE_DIR / ".env.db",
            BASE_DIR / ".env.admin",
            BASE_DIR / ".env.api",
        ),
    )

    redis: RedisConfig
    db: DatabaseConfig
    admin: AdminConfig
    api: ApiConfig
    token_timeout: int = 600


# noinspection PyArgumentList
settings = Settings()
