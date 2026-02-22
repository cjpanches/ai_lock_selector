from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "AI Lock Selector"
    debug: bool = True
    
    database_url: str = "sqlite+aiosqlite:///./locks.db"
    
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
