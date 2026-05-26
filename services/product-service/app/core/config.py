from functools import lru_cache
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    service_name: str = 'product-service'
    environment: str = 'local'
    database_url: str = 'sqlite:///./products.db'
    cors_origins: str = 'http://localhost:3000'
    class Config:
        env_file = '.env'
        extra = 'ignore'
@lru_cache
def get_settings() -> Settings:
    return Settings()
