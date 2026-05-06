"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CAEP Holding Administration API"
    app_version: str = "0.1.0"
    environment: str = "local"
    debug: bool = Field(default=False, validation_alias="APP_DEBUG")

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "caep_holding"
    postgres_user: str = "caep"
    postgres_password: str = "caep"
    database_url: str | None = Field(default=None, validation_alias="DATABASE_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url

        return (
            "postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
