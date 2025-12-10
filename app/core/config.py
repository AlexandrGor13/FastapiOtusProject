import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

env = os.getenv("ENV_STATE")

BASE_DIR = Path(__file__).resolve().parent.parent

SQLA_PG_ASYNC_ENGINE = "asyncpg"


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / f".env.{env}", env_file_encoding="utf-8", extra="ignore"
    )


class RedisConfig(ConfigBase):
    """
    Setting for Redis
    """

    model_config = SettingsConfigDict(env_prefix="redis_")
    db: int = 0
    host: str
    port: int


class ApiConfig(ConfigBase):
    """
    Setting for the API
    """

    model_config = SettingsConfigDict(env_prefix="api_")
    secret_key: str
    kandinsky_host: str
    kandinsky_port: int
    deepface_host: str
    deepface_port: int


class AdminConfig(ConfigBase):
    """
    Setting for the AdminPanel
    """

    model_config = SettingsConfigDict(env_prefix="admin_")
    user: str
    password: str


class DatabaseConfig(ConfigBase):
    """
    Setting for the PostgreSQL database
    """

    model_config = SettingsConfigDict(env_prefix="db_")
    name: str
    user: str
    password: str
    host: str
    port: int

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
        env_file=(BASE_DIR / ".env.prod"),
    )

    redis: RedisConfig = Field(default_factory=RedisConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    admin: AdminConfig = Field(default_factory=AdminConfig)
    api: ApiConfig = Field(default_factory=ApiConfig)
    token_timeout: int = 600


# noinspection PyArgumentList
settings = Settings()  # type: ignore[call-arg]
