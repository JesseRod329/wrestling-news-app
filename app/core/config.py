from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Real Wrestling News"
    environment: str = "dev"  # dev | test | prod

    # Database
    database_url: str = "sqlite:///./dev.db"
    
    def get_database_url(self) -> str:
        """Get database URL, defaulting to PostgreSQL in production"""
        if self.environment == "prod" and "postgresql://" not in self.database_url:
            # In production, expect DATABASE_URL environment variable
            import os
            return os.getenv("DATABASE_URL", self.database_url)
        return self.database_url

    # Security
    jwt_secret_key: str = "change-me"  # do not use in prod
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    # Credibility thresholds
    credibility_confirmed_threshold: float = 0.7
    credibility_rumor_threshold: float = 0.3
    credibility_wilson_weight: float = 0.7
    credibility_source_weight: float = 0.3

    # Elasticsearch (optional initially)
    elastic_cloud_id: str | None = None
    elastic_api_key: str | None = None

    class Config:
        env_file = ".env"
        env_prefix = "APP_"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


