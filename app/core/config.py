from pydantic import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DNS: str
    WHATSAPP_INSTANCE_ID: str
    WHATSAPP_API_TOKEN: str
    WHATSAPP_BASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
