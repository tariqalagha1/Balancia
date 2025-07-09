from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/balancia"
    
    # Auth
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email
    SMTP_SERVER: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "your-email@example.com"
    SMTP_PASSWORD: str = "your-email-password"
    EMAIL_FROM: str = "noreply@example.com"
    
    # App
    FRONTEND_URL: str = "http://localhost:3000"
    APP_NAME: str = "Balancia"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()