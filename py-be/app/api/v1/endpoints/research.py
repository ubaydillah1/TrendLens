"""HTTP endpoints for triggering TrendLens AI research operations."""

from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from app.schemas.research import ResearchRequest, ResearchResponse
from app.services.research_service import research_service

router = APIRouter()


@router.post(
    "/run",
    response_model=ResearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Trigger synchronous daily research",
)
async def trigger_research(payload: ResearchRequest) -> ResearchResponse:
    """Executes the full News-First AI research pipeline and returns the synthesized report.

    Args:
        payload: Creator niche and positioning preferences.

    Returns:
        Structured response containing categorized content ideas and viral hooks.
    """
    return await research_service.execute_research(payload)


@router.post(
    "/stream",
    summary="Stream research execution progress via Server-Sent Events",
)
async def stream_research_progress(payload: ResearchRequest) -> StreamingResponse:
    """Streams real-time node transitions and status updates using Server-Sent Events (SSE).

    Args:
        payload: Creator niche and positioning preferences.

    Returns:
        StreamingResponse yielding text/event-stream chunks for each pipeline phase.
    """
    return StreamingResponse(
        research_service.stream_research(payload),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
