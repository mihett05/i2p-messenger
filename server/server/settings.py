from functools import lru_cache
from pydantic import BaseSettings
from datetime import timedelta


class Settings(BaseSettings):
    DATABASE_URL = "sqlite:///db.sqlite"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRE = timedelta(days=30)
    JWT_SECRET_KEY = "super-mega-secret"


@lru_cache
def get_settings() -> Settings:
    return Settings()
