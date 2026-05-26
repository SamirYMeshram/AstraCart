from functools import lru_cache
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str = 'order-service'
    database_url: str = 'sqlite:///./orders.db'
    cart_service_url: str = 'http://cart-service:8000'
    product_service_url: str = 'http://product-service:8000'
    notification_service_url: str = 'http://notification-service:8000'
    cors_origins: str = 'http://localhost:3000'
    class Config: env_file='.env'; extra='ignore'
@lru_cache
def get_settings(): return Settings()
