import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

APP_ENV = os.getenv("APP_ENV", "dev")


class Settings(BaseSettings):
    PROJECT_NAME: str = "mlinks"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/dbname"
    REDIS_URL: str = "redis://localhost:6379/0"

    LOG_LEVEL: str = "ERROR"
    LOG_FILE_PATH: str = "./logs/app.log"

    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    SECRET_KEY: str = "your-super-secret-key-that-is-at-least-32-bytes-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(env_file=f".env.{APP_ENV}", extra="ignore", env_file_encoding="utf-8")


@lru_cache
def get_settings_instance() -> Settings:
    return Settings()


settings = get_settings_instance()
