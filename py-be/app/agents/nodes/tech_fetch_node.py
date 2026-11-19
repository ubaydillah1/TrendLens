"""Node for fetching live technical news and engineering discussions."""

from typing import Any

from app.agents.states.research_state import ResearchAgentState
from app.agents.tools.tech_news import fetch_top_tech_news


def tech_fetch_node(state: ResearchAgentState) -> dict[str, Any]:
    """LangGraph node that ingests live technical discussions into state.

    Fetches current high-engagement engineering topics from Hacker News
    and populates 'tech_news_raw' if not already provided.

    Args:
        state: Current graph state.

    Returns:
        Partial state dictionary updating 'tech_news_raw'.
    """
    # If raw news is already supplied (e.g. in test fixtures), keep it
    if state.get("tech_news_raw"):
        return {"tech_news_raw": state["tech_news_raw"]}

    live_news = fetch_top_tech_news(limit=8, min_points=25)
    return {"tech_news_raw": live_news}