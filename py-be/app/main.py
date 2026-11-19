"""FastAPI application entrypoint and middleware configuration."""

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.v1.router import api_router
from app.core.config import settings
from fastapi import FastAPI


def create_application() -> FastAPI:
    """Creates and configures the FastAPI application instance."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Allow cross-origin requests from frontend and local microservices
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register centralized v1 API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/api/v1/docs", include_in_schema=False)
    async def redirect_api_docs() -> RedirectResponse:
        """Redirects v1 docs path to standard swagger docs."""
        return RedirectResponse(url="/docs")

    @app.get("/", summary="Root health & metadata status")
    async def root_index() -> dict[str, str]:
        """Provides basic metadata and links to API documentation."""
        return {
            "name": settings.PROJECT_NAME,
            "version": "1.0.0",
            "docs": "/docs",
        }

    return app


app = create_application()
