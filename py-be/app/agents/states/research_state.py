from typing import Any, TypedDict


class ResearchAgentState(TypedDict):
    niche: str
    user_positioning: str
    viral_trends_raw: list[dict[str, Any]]
    tech_news_raw: list[dict[str, Any]]
    final_report: dict[str, Any]
