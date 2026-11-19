"""Tool for fetching trending technical news, engineering debates, and community discussions."""

from typing import Any

import httpx

HACKER_NEWS_API_URL = "https://hn.algolia.com/api/v1/search"
LOBSTERS_HOTTEST_URL = "https://lobste.rs/hottest.json"


def fetch_top_tech_news(limit: int = 25, min_points: int = 15) -> list[dict[str, Any]]:
    """Fetches high-engagement engineering discussions from Hacker News and Lobste.rs.

    Combines global tech front-page news with senior systems engineering debates,
    capturing both the underlying article URL and the community comments discussion link.

    Args:
        limit: Maximum total news stories to return.
        min_points: Minimum upvotes/points threshold for inclusion.

    Returns:
        List of structured dictionaries containing topic titles, source URLs,
        discussion URLs, and engagement metrics.
    """
    news_items: list[dict[str, Any]] = []

    # 1. Fetch Hacker News front-page debates
    try:
        hn_params = {
            "tags": "front_page",
            "hitsPerPage": 25,
        }
        hn_resp = httpx.get(HACKER_NEWS_API_URL, params=hn_params, timeout=10.0)
        if hn_resp.status_code == 200:
            hits = hn_resp.json().get("hits", [])
            for hit in hits:
                points = hit.get("points") or 0
                if points < min_points:
                    continue
                title = hit.get("title")
                if not title:
                    continue

                object_id = hit.get("objectID")
                discussion_url = f"https://news.ycombinator.com/item?id={object_id}"
                article_url = hit.get("url") or discussion_url

                news_items.append(
                    {
                        "source": "HackerNews",
                        "topic": title,
                        "article_url": article_url,
                        "discussion_url": discussion_url,
                        "engagement_score": points,
                        "comments_count": hit.get("num_comments") or 0,
                    }
                )
    except Exception:
        pass

    # 2. Fetch Lobste.rs senior engineering discussions
    try:
        lob_resp = httpx.get(
            LOBSTERS_HOTTEST_URL,
            timeout=10.0,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
        if lob_resp.status_code == 200:
            lob_stories = lob_resp.json()
            for story in lob_stories[:15]:
                score = story.get("score") or 0
                title = story.get("title")
                if not title:
                    continue

                news_items.append(
                    {
                        "source": "Lobsters",
                        "topic": title,
                        "article_url": story.get("url") or story.get("comments_url"),
                        "discussion_url": story.get("comments_url") or "",
                        "engagement_score": score,
                        "comments_count": story.get("comment_count") or 0,
                    }
                )
    except Exception:
        pass

    # Sort all stories by engagement score descending to prioritize high-gravity topics
    news_items.sort(key=lambda x: x.get("engagement_score", 0), reverse=True)
    return news_items[:limit]
