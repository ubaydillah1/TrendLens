"""Tool for querying trending technical videos and viral hooks from YouTube."""

from typing import Any

import yt_dlp


def search_youtube_trends(query: str, limit: int = 6) -> list[dict[str, Any]]:
    """Searches YouTube for trending videos matching a topic without requiring API keys.

    Leverages yt-dlp flat metadata extraction to retrieve video titles, channel names,
    view counts, and canonical URLs.

    Args:
        query: Search keywords (e.g., 'software engineering trends 2026').
        limit: Maximum number of search results to retrieve.

    Returns:
        List of structured dictionaries representing trending video metadata.
    """
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
        "no_warnings": True,
    }

    search_term = f"ytsearch{limit}:{query}"
    results: list[dict[str, Any]] = []

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            extracted_info = ydl.extract_info(search_term, download=False)
            if not extracted_info:
                return []

            entries = extracted_info.get("entries", [])
            for entry in entries:
                if not entry:
                    continue

                title = entry.get("title")
                if not title:
                    continue

                video_id = entry.get("id")
                source_url = entry.get("url") or (
                    f"https://www.youtube.com/watch?v={video_id}" if video_id else None
                )

                if not source_url:
                    continue

                results.append(
                    {
                        "platform": "YouTube",
                        "title": title,
                        "views": entry.get("view_count") or 0,
                        "channel": entry.get("channel") or entry.get("uploader") or "Unknown",
                        "source_url": source_url,
                    }
                )
    except Exception:
        # Fallback gracefully if YouTube blocks or network fails
        return []

    return results
