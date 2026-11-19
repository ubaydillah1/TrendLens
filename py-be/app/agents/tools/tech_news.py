"""Tool for fetching trending technical news and engineering debates."""

from typing import Any

import httpx

HACKER_NEWS_API_URL = "https://hn.algolia.com/api/v1/search"


def fetch_top_tech_news(limit: int = 10, min_points: int = 25) -> list[dict[str, Any]]:
    """Fetches high-engagement stories and debates from Hacker News.

    Queries the Algolia Hacker News front page API, filtering for posts with
    high developer engagement (points and comments).

    Args:
        limit: Maximum number of news stories to return.
        min_points: Minimum upvotes threshold to qualify as trending.

    Returns:
        List of structured dictionaries containing topic titles, URLs, and engagement scores.
    """
    params = {
        "tags": "front_page",
        "hitsPerPage": limit * 2,  # Fetch extra to account for filtering
    }

    try:
        response = httpx.get(HACKER_NEWS_API_URL, params=params, timeout=10.0)
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError:
        # Fallback gracefully if external network request fails
        return []

    hits = data.get("hits", [])
    news_items: list[dict[str, Any]] = []

    for hit in hits:
        points = hit.get("points") or 0
        if points < min_points:
            continue

        title = hit.get("title")
        if not title:
            continue

        object_id = hit.get("objectID")
        source_url = hit.get("url") or f"https://news.ycombinator.com/item?id={object_id}"
        num_comments = hit.get("num_comments") or 0

        news_items.append(
            {
                "source": "HackerNews",
                "topic": title,
                "url": source_url,
                "engagement_score": points,
                "comments_count": num_comments,
            }
        )

        if len(news_items) >= limit:
            break

    return news_items
