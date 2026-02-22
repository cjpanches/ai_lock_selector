from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    app_name: str = "AI Lock Selector"
    debug: bool = True
    
    database_url: str = "postgresql://ailock:ailock_password@localhost:5432/ailock_db"
    
    cors_origins: list = ["*"]


def get_settings():
    if os.environ.get("TESTING"):
        return Settings(database_url="sqlite+aiosqlite:///./test_locks.db")
    return Settings()

settings = get_settings()
