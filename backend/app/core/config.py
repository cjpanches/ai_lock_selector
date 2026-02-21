from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "AI Lock Selector"
    debug: bool = True
    
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/locks"
    
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
