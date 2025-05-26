from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "API Lu Estilo"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://marcos:admin@localhost/lu_estilo"
    JWT_SECRET_KEY: str = "IG6JZ9itEk90eGqk7BgYEq5ul0rXPSILSrvUgLudGPf75ah1jPqLKiHn40jejIlqSCW5B7ddAoIaV198fIT9vQ"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    WHATSAPP_INSTANCE_ID: str
    WHATSAPP_API_TOKEN: str
    WHATSAPP_BASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
