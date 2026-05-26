from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    service_name: str = 'user-service'
    environment: str = 'local'
    database_url: str = 'sqlite:///./users.db'
    jwt_secret_key: str = 'change-me'
    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14
    cors_origins: str = 'http://localhost:3000'
    notification_service_url: str = 'http://notification-service:8000'

    class Config:
        env_file = '.env'
        extra = 'ignore'

@lru_cache
def get_settings() -> Settings:
    return Settings()
