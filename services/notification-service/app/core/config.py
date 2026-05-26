from functools import lru_cache
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str='notification-service'
    database_url: str='sqlite:///./notifications.db'
    celery_broker_url: str='redis://redis:6379/1'
    celery_result_backend: str='redis://redis:6379/2'
    cors_origins: str='http://localhost:3000'
    class Config: env_file='.env'; extra='ignore'
@lru_cache
def get_settings(): return Settings()
