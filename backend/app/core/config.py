from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    
    app_name: str = "AI Lock Selector"
    debug: bool = True
    
    database_url: str = "sqlite+aiosqlite:///./locks.db"
    
    cors_origins: list = ["*"]


@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
