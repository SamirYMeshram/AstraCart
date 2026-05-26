from functools import lru_cache
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str='api-gateway'
    jwt_secret_key: str='change-me'
    jwt_algorithm: str='HS256'
    redis_url: str='redis://redis:6379/0'
    user_service_url: str='http://user-service:8000'
    product_service_url: str='http://product-service:8000'
    cart_service_url: str='http://cart-service:8000'
    order_service_url: str='http://order-service:8000'
    payment_service_url: str='http://payment-service:8000'
    notification_service_url: str='http://notification-service:8000'
    cors_origins: str='http://localhost:3000'
    class Config: env_file='.env'; extra='ignore'
@lru_cache
def get_settings(): return Settings()
