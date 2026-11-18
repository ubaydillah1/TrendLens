from typing import Any, TypedDict


class ResearchAgentState(TypedDict):
    niche: str
    user_positioning: str
    # Raw data inputs (mocked today, real scrapers later)
    viral_trends_raw: list[dict[str, Any]]
    tech_news_raw: list[dict[str, Any]]
    # Output produced by the synthesis node
    final_report: dict[str, Any]
