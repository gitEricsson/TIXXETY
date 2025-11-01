from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    app_name: str = "TIXXETY"
    env: str = "dev"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"

    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/tixxety"
    sync_database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/tixxety"

    redis_url: str = "redis://redis:6379/0"
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"

    ticket_reservation_ttl_seconds: int = 120

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Singleton instance for convenient import
settings = get_settings()
