from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "Donna API"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()