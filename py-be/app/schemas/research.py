from pydantic import BaseModel, Field


class ContentIdea(BaseModel):
    category: str = Field(
        description="Content bucket, e.g., 'Debate / Hot Take', 'Utility Hack', 'Career Reality', 'Architecture Deep-Dive'"
    )
    topic_title: str = Field(description="Clear, punchy concept title for the video")
    viral_hooks: list[str] = Field(
        description="2-3 variations of the first 3-second spoken opening hook in conversational Indonesian"
    )
    visual_hook_direction: str = Field(
        description="Visual action on camera/screen in the first 3 seconds (e.g., 'Show terminal with failing curl', 'Screen record cloud cost spike')"
    )
    content_outline: list[str] = Field(
        description="3-4 bullet points detailing the core technical message, trade-off, or architectural solution"
    )
    technical_datapoint: str = Field(
        description="Specific metric, CVE code, benchmark figure, or hard data point to cite in the video"
    )
    engagement_cta: str = Field(
        description="Spoken closing question or call-to-action designed to trigger debates in the comments section"
    )
    why_it_works: str = Field(
        description="Psychological trigger (e.g., Curiosity gap, Contrarian take, Cost shock, FOMO)"
    )
    source_technical_topic: str = Field(
        description="The underlying technical topic or issue"
    )
    news_source_url: str = Field(
        description="Primary news article or technical advisory URL for creator research"
    )
    community_discussion_url: str = Field(
        description="URL to the community comments/debate thread (Hacker News or Lobsters) to see real developer reactions"
    )
    inspiration_video_url: str = Field(
        description="URL of the trending YouTube video that inspired the hook structure"
    )


class SearchQueries(BaseModel):
    queries: list[str] = Field(
        description="List of 3 diverse, high-intent YouTube search queries targeting different emotional angles"
    )


class DailyResearchReport(BaseModel):
    date: str = Field(description="ISO Date of generation")
    target_niche: str = Field(
        description="Target niche, e.g., 'AI & Software Engineering'"
    )
    user_positioning: str = Field(
        description="The persona applied, e.g., 'Pragmatic Senior Engineer with sarcastic tone'"
    )
    ideas: list[ContentIdea] = Field(
        description="Strictly 10 distinct, non-repetitive content ideas from 10 different technical topics"
    )


class ResearchRequest(BaseModel):
    """Payload schema for triggering research pipeline execution."""

    niche: str = Field(
        default="AI & Software Engineering",
        description="Primary content domain and technical focus",
        examples=["AI & Software Engineering"],
    )
    user_positioning: str = Field(
        default="Pragmatic Senior Backend Engineer, skeptical of AI hype, focuses on real architecture and cost efficiency",
        description="Creator voice, tone, and strategic content perspective",
        examples=[
            "Pragmatic Senior Backend Engineer, skeptical of AI hype, focuses on real architecture and cost efficiency"
        ],
    )


class ResearchResponse(BaseModel):
    """Standard API response schema for synchronous research executions."""

    success: bool = Field(default=True, description="Execution success indicator")
    message: str = Field(
        default="Research pipeline completed successfully",
        description="Informational status message",
    )
    data: DailyResearchReport = Field(
        description="Final synthesized research report and content ideas"
    )
