from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "API Lu Estilo"
    VERSION: str = "1.0.0"
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    WHATSAPP_INSTANCE_ID: str
    WHATSAPP_API_TOKEN: str
    WHATSAPP_BASE_URL: str
    DNS: str

    class Config:
        env_file = ".env"  
settings = Settings()
