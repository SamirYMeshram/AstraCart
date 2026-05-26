from functools import lru_cache
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str='payment-service'
    database_url: str='sqlite:///./payments.db'
    order_service_url: str='http://order-service:8000'
    notification_service_url: str='http://notification-service:8000'
    cors_origins: str='http://localhost:3000'
    class Config: env_file='.env'; extra='ignore'
@lru_cache
def get_settings(): return Settings()
