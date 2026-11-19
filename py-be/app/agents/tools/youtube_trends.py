"""Tool for querying trending technical videos and extracting spoken transcript hooks."""

import html
import re
from typing import Any

import yt_dlp

VTT_TIME_RE: re.Pattern = re.compile(
    r"^(?:\d{2,}:)?\d{2}:\d{2}\.\d{3}[ \t]+-->[ \t]+(?:\d{2,}:)?\d{2}:\d{2}\.\d{3}(?:[ \t]|$)"
)
TAG_RE: re.Pattern = re.compile(r"<[^>]+>")


def vtt_to_text(vtt_content: str) -> str:
    """Parses raw WebVTT subtitle data into continuous readable plain text."""
    cleaned_lines: list[str] = []
    in_cue: bool = False

    for raw_line in vtt_content.splitlines():
        line = raw_line.strip()
        if not line:
            in_cue = False
            continue

        if VTT_TIME_RE.match(line):
            in_cue = True
            continue

        if not in_cue:
            continue

        text = html.unescape(TAG_RE.sub("", line)).strip()
        if text and (not cleaned_lines or cleaned_lines[-1] != text):
            cleaned_lines.append(text)

    return " ".join(cleaned_lines)


def get_transcript(
    info: dict[str, Any],
    ydl: yt_dlp.YoutubeDL,
    preferred_langs: tuple[str, ...] = ("id", "en", "en-orig"),
) -> str | None:
    """Retrieves and cleans subtitles/captions from video metadata in priority order."""
    caption_sources = (
        info.get("subtitles") or {},
        info.get("automatic_captions") or {},
    )

    for source in caption_sources:
        for lang in preferred_langs:
            tracks: list[dict[str, Any]] = source.get(lang) or []
            vtt_track = next((t for t in tracks if t.get("ext") == "vtt"), None)
            if vtt_track and "url" in vtt_track:
                raw_bytes = ydl.urlopen(vtt_track["url"]).read()
                raw_vtt = raw_bytes.decode("utf-8", errors="replace")
                return vtt_to_text(raw_vtt)

    return None


def extract_youtube_transcript(url: str, max_words: int = 80) -> str | None:
    """Extracts the opening spoken hook from a video transcript without downloading media.

    Args:
        url: Direct YouTube video URL.
        max_words: Number of leading words to extract for the verbal hook analysis.

    Returns:
        Spoken transcript excerpt string, or None if unavailable.
    """
    ydl_opts: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return None
            full_transcript = get_transcript(info, ydl)
            if not full_transcript:
                return None
            words = full_transcript.split()
            return " ".join(words[:max_words])
    except Exception:
        return None


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
