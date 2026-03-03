import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "SMHunt Client Acquisition Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./smhunt.db")
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # API Keys
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    SENDGRID_API_KEY: Optional[str] = None
    MAILGUN_API_KEY: Optional[str] = None
    HUNTER_API_KEY: Optional[str] = None
    CLEARBIT_API_KEY: Optional[str] = None

    # Email Configuration
    SMTP_HOST: str = "smtp.sendgrid.net"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "apikey"
    SMTP_PASSWORD: Optional[str] = None
    DEFAULT_FROM_EMAIL: str = "noreply@smhunt.online"
    DEFAULT_FROM_NAME: str = "SMHunt Lead Intelligence"

    # Security
    SECRET_KEY: str = "your-default-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Frontend Configuration
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"

    # Business Parameters
    DEFAULT_COUNTRY: str = "USA"
    DEFAULT_CITY: str = "New York"
    DEFAULT_NICHE: str = "Dental Clinics"
    DEFAULT_SERVICE_TYPE: str = "Digital Marketing"

    # Rate Limiting
    API_RATE_LIMIT: str = "100/minute"
    EMAIL_RATE_LIMIT: str = "500/day"

    # Monitoring
    SENTRY_DSN: Optional[str] = None

    # Production Settings
    WORKERS_PER_CORE: str = "1"
    WEB_CONCURRENCY: str = "1"
    HOST: str = "0.0.0.0"
    PORT: str = "8000"
    LOG_LEVEL: str = "INFO"
    WORKER_CLASS: str = "uvicorn.workers.UvicornWorker"
    MAX_WORKERS: str = "8"
    TIMEOUT: str = "120"
    KEEP_ALIVE: str = "5"
    GRACEFUL_TIMEOUT: str = "120"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "allow"


# Create settings instance
settings = Settings()
