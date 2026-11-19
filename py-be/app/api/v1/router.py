"""Central API router aggregating all v1 feature endpoints."""

from app.api.v1.endpoints import health, research
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(research.router, prefix="/research", tags=["Research"])
