"""Service layer orchestrating the AI research pipeline and streaming events."""

import asyncio
import json
from collections.abc import AsyncGenerator
from typing import Any

from app.agents.graphs.research_graph import research_graph
from app.schemas.research import (
    DailyResearchReport,
    ResearchRequest,
    ResearchResponse,
)


class ResearchService:
    """Orchestrates research executions between API handlers and the AI agent graph."""

    async def execute_research(self, request: ResearchRequest) -> ResearchResponse:
        """Executes the research graph synchronously and returns the complete report.

        Args:
            request: Validated input containing niche and user positioning.

        Returns:
            Structured response wrapping the synthesized research report.
        """
        graph_input = {
            "niche": request.niche,
            "user_positioning": request.user_positioning,
        }

        # Run within threadpool to prevent blocking the async event loop during scraping
        result = await asyncio.to_thread(research_graph.invoke, graph_input)
        report_data = result.get("final_report") or {}

        validated_report = DailyResearchReport.model_validate(report_data)

        return ResearchResponse(
            success=True,
            message="Research pipeline completed successfully",
            data=validated_report,
        )

    async def stream_research(
        self, request: ResearchRequest
    ) -> AsyncGenerator[str, None]:
        """Streams real-time execution steps and node updates via Server-Sent Events.

        Yields SSE-compliant string chunks whenever a graph node completes its task.

        Args:
            request: Validated input containing niche and user positioning.

        Yields:
            Formatted SSE data chunks (e.g., 'data: {...}\\n\\n').
        """
        graph_input = {
            "niche": request.niche,
            "user_positioning": request.user_positioning,
        }

        # Initial connection acknowledgement
        initial_event = {
            "step": "started",
            "message": "Initializing TrendLens News-First Research Pipeline",
        }
        yield f"data: {json.dumps(initial_event)}\n\n"

        # Stream graph node transitions asynchronously
        async for output in research_graph.astream(graph_input, stream_mode="updates"):
            for node_name, state_update in output.items():
                event_payload: dict[str, Any] = {
                    "step": node_name,
                    "status": "completed",
                }

                if node_name == "fetch_tech_news":
                    news = state_update.get("tech_news_raw", [])
                    event_payload["message"] = f"Ingested {len(news)} breaking engineering topics from Hacker News"
                    event_payload["data"] = [item.get("topic") for item in news[:5]]

                elif node_name == "query_planner":
                    queries = state_update.get("search_queries", [])
                    event_payload["message"] = f"Planned {len(queries)} grounded video search queries"
                    event_payload["data"] = queries

                elif node_name == "fetch_viral_trends":
                    trends = state_update.get("viral_trends_raw", [])
                    event_payload["message"] = f"Ingested {len(trends)} viral video trends & spoken opening hooks"
                    event_payload["data"] = [
                        {"title": t.get("title"), "views": t.get("views")}
                        for t in trends[:5]
                    ]

                elif node_name == "synthesis":
                    report = state_update.get("final_report", {})
                    event_payload["message"] = "Cross-synthesis complete! Generated final content cards"
                    event_payload["data"] = report

                yield f"data: {json.dumps(event_payload, ensure_ascii=False)}\n\n"

        completion_event = {
            "step": "done",
            "message": "Pipeline execution finished successfully",
        }
        yield f"data: {json.dumps(completion_event)}\n\n"


research_service = ResearchService()
