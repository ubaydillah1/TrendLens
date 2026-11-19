"""Centralized configuration management for TrendLens AI service."""

import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Ensure .env is resolved regardless of whether execution starts from root or py-be
load_dotenv(find_dotenv())


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
        env_file=find_dotenv(),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
