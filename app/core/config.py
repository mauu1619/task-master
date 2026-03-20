from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_URL: str = Field(default=...)
    SECRET_KEY: str = Field(default=...)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings() 