"""Health check endpoints for service monitoring and container orchestrators."""

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz", summary="Service health status")
async def health_check() -> dict[str, Any]:
    """Returns basic service health status for Docker and orchestrator probes."""
    return {
        "status": "healthy",
        "service": "trendlens-ai",
    }
