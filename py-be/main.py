"""Application root wrapper exporting the configured FastAPI application instance."""

from app.main import app

__all__ = ["app"]
