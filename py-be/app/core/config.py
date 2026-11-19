"""Centralized configuration management for TrendLens AI service."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings validated via pydantic-settings."""

    PROJECT_NAME: str = "TrendLens AI Research Engine"
    API_V1_STR: str = "/api/v1"
    OPENAI_API_KEY: str = ""
    DATABASE_URL: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/trendlens_ai"
    )
    PORT: int = 8001

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
