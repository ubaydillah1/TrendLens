"""Node for ingesting live trending video formats and hooks from YouTube."""

from typing import Any

from app.agents.states.research_state import ResearchAgentState
from app.agents.tools.youtube_trends import (
    extract_youtube_transcript,
    search_youtube_trends,
)


def viral_fetch_node(state: ResearchAgentState) -> dict[str, Any]:
    """LangGraph node that ingests trending video metadata using planned search queries.

    Executes search queries planned by the query planner, deduplicates videos
    by URL, and extracts opening spoken transcript hooks for top candidates.

    Args:
        state: Current graph state containing 'search_queries' or fallback 'niche'.

    Returns:
        Partial state dictionary updating 'viral_trends_raw'.
    """
    if state.get("viral_trends_raw"):
        return {"viral_trends_raw": state["viral_trends_raw"]}

    queries = state.get("search_queries") or []
    if not queries:
        niche = state.get("niche", "software engineering")
        queries = [f"{niche} trends 2026"]

    collected_trends: list[dict[str, Any]] = []
    seen_urls: set[str] = set()

    for query in queries:
        results = search_youtube_trends(query=query, limit=3)
        query_top_hook_extracted = False

        for item in results:
            url = item.get("source_url")
            if url and url not in seen_urls:
                seen_urls.add(url)
                item["discovered_via_query"] = query

                # Extract the opening verbal hook for the first unique video per query
                if not query_top_hook_extracted:
                    item["transcript_hook"] = extract_youtube_transcript(url, max_words=80)
                    query_top_hook_extracted = True
                else:
                    item["transcript_hook"] = None

                collected_trends.append(item)

    return {"viral_trends_raw": collected_trends}
