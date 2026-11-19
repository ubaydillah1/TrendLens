"""Node for ingesting live trending video formats and hooks from YouTube."""

from typing import Any

from app.agents.states.research_state import ResearchAgentState
from app.agents.tools.youtube_trends import search_youtube_trends


def viral_fetch_node(state: ResearchAgentState) -> dict[str, Any]:
    """LangGraph node that ingests trending video metadata using planned search queries.

    Executes search queries planned by the query planner, deduplicating videos
    by URL to ensure diverse, high-performing coverage.

    Args:
        state: Current graph state containing 'search_queries' or fallback 'niche'.

    Returns:
        Partial state dictionary updating 'viral_trends_raw'.
    """
    # If raw trends are already provided (e.g. testing fixtures), preserve them
    if state.get("viral_trends_raw"):
        return {"viral_trends_raw": state["viral_trends_raw"]}

    queries = state.get("search_queries") or []
    if not queries:
        niche = state.get("niche", "software engineering")
        queries = [f"{niche} trends 2026"]

    collected_trends: list[dict[str, Any]] = []
    seen_urls: set[str] = set()

    for query in queries:
        # Fetch top 2-3 videos per query to maintain diversity
        results = search_youtube_trends(query=query, limit=3)
        for item in results:
            url = item.get("source_url")
            if url and url not in seen_urls:
                seen_urls.add(url)
                # Tag the query that led to this video discovery for transparency
                item["discovered_via_query"] = query
                collected_trends.append(item)

    return {"viral_trends_raw": collected_trends}
