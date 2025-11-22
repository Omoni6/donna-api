import os
from typing import List, Optional
from pydantic import validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Donna API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    API_KEY: str = os.getenv("API_KEY", "donna-api-key-production")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "jwt-secret-key")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "https://app.omoni.fr",
        "https://dashboard.omoni.fr",
        "https://www.omoni.fr"
    ]
    ALLOWED_HOSTS: List[str] = ["*"]  # Configurer selon ton domaine
    
    # Services URLs
    DONNA_WORKER_URL: str = os.getenv("DONNA_WORKER_URL", "http://donna:8001/api/donna/run")
    
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    TELEGRAM_DONNA_BOT_TOKEN: str = os.getenv("TELEGRAM_DONNA_BOT_TOKEN", "")
    TELEGRAM_BOT_USERNAME: str = os.getenv("TELEGRAM_BOT_USERNAME", "")
    TELEGRAM_API_ID: str = os.getenv("TELEGRAM_API_ID", "")
    TELEGRAM_API_HASH: str = os.getenv("TELEGRAM_API_HASH", "")
    TELEGRAM_API_KEY: str = os.getenv("TELEGRAM_API_KEY", "")
    TELEGRAM_WEBHOOK_URL: str = os.getenv("TELEGRAM_WEBHOOK_URL", "")
    TELEGRAM_NOTIFICATIONS: bool = os.getenv("TELEGRAM_NOTIFICATIONS", "true").lower() == "true"
    
    # Telegram Channels & Groups
    TELEGRAM_AUDIT_CHANNEL_ID: str = os.getenv("TELEGRAM_AUDIT_CHANNEL_ID", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    TELEGRAM_CHAT_ID_ALERTS: str = os.getenv("TELEGRAM_CHAT_ID_ALERTS", "")
    TELEGRAM_CHAT_ID_SYSTEM: str = os.getenv("TELEGRAM_CHAT_ID_SYSTEM", "")
    TELEGRAM_CHAT_ID_TEAM: str = os.getenv("TELEGRAM_CHAT_ID_TEAM", "")
    TELEGRAM_CHAT_ID_REPORTS: str = os.getenv("TELEGRAM_CHAT_ID_REPORTS", "")
    TELEGRAM_CHAT_ID_MARKETING: str = os.getenv("TELEGRAM_CHAT_ID_MARKETING", "")
    
    # Slack Configuration
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_SIGNING_SECRET: str = os.getenv("SLACK_SIGNING_SECRET", "")
    SLACK_APP_ID: str = os.getenv("SLACK_APP_ID", "")
    SLACK_TEAM_ID: str = os.getenv("SLACK_TEAM_ID", "")
    
    # Slack Channels
    SLACK_CHANNEL_TEAM: str = os.getenv("SLACK_CHANNEL_TEAM", "")
    SLACK_CHANNEL_ALERTS: str = os.getenv("SLACK_CHANNEL_ALERTS", "")
    SLACK_CHANNEL_CRM: str = os.getenv("SLACK_CHANNEL_CRM", "")
    
    # Stripe Configuration
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    GOOGLE_SERVICE_ACCOUNT_KEY: str = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY", "")
    
    # Default channels for testing
    DEFAULT_TELEGRAM_CHAT_ID: str = os.getenv("DEFAULT_TELEGRAM_CHAT_ID", "")
    DEFAULT_SLACK_CHANNEL: str = os.getenv("DEFAULT_SLACK_CHANNEL", "general")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./donna.db")
    
    # Redis / Cache
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: str = os.getenv("LOG_DIR", "/app/logs")
    
    # Multi-tenant
    TENANT_ID_HEADER: str = "X-Tenant-ID"
    DEFAULT_TENANT: str = "omoni"
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()