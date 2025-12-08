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
    host: str = "localhost"
    port: int = 6379


class ApiConfig(BaseModel):
    """
    Setting for the API
    """

    secret_key: str = "my_secret_key"
    kandinsky_host: str = "kandinsky"
    kandinsky_port: int = 8001
    deepface_host: str = "deepface"
    deepface_port: int = 8002


class AdminConfig(BaseModel):
    """
    Setting for the AdminPanel
    """

    user: str = "admin"
    password: str = "password"


class DatabaseConfig(BaseModel):
    """
    Setting for the PostgreSQL database
    """

    name: str = "postgres"
    user: str = "postgres"
    password: str = "password"
    host: str = "localhost"
    port: int = 5432

    pool_size: int = 10
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
        env_file=(BASE_DIR / ".env", BASE_DIR / ".env.template"),
    )

    redis: RedisConfig = RedisConfig()
    db: DatabaseConfig = DatabaseConfig()
    admin: AdminConfig = AdminConfig()
    api: ApiConfig = ApiConfig()
    token_timeout: int = 600


# noinspection PyArgumentList
settings = Settings()  # type: ignore[call-arg]
