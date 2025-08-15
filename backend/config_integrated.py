import os
from pathlib import Path
from pydantic_settings import BaseSettings

class IntegratedSettings(BaseSettings):
    """Settings for the integrated wrestling platform"""
    
    # Environment
    environment: str = "dev"
    
    # Database
    database_url: str = "sqlite:///./integrated_wrestling.db"
    
    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS
    cors_origins: list = ["*"]
    
    # News settings
    news_poll_interval: int = 900  # 15 minutes
    
    # Stats settings
    stats_cache_ttl: int = 3600  # 1 hour
    
    # File paths
    base_dir: Path = Path(__file__).parent.parent
    newsite_dir: Path = base_dir / ".." / "newsite"
    static_dir: Path = base_dir / "static"
    
    class Config:
        env_file = ".env"
        env_prefix = "INTEGRATED_"

def get_integrated_settings() -> IntegratedSettings:
    """Get integrated application settings"""
    return IntegratedSettings()

# Create settings instance
settings = get_integrated_settings()
