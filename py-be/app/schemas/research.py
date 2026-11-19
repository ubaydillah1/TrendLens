from pydantic import BaseModel, Field


class ContentIdea(BaseModel):
    category: str = Field(
        description="Content bucket, e.g., 'Debate / Hot Take', 'Utility Hack', 'Career Reality'"
    )
    topic_title: str = Field(description="Clear, punchy concept title for the video")
    viral_hooks: list[str] = Field(
        description="2-3 variations of the first 3-second opening hook"
    )
    content_outline: list[str] = Field(
        description="3-4 bullet points explaining the core message of the video"
    )
    why_it_works: str = Field(
        description="Psychological trigger or viral reasoning (e.g., Curiosity gap, Contrarian)"
    )
    source_technical_topic: str = Field(
        description="The underlying technical topic or issue (e.g., Go memory leak)"
    )
    source_reference_url: str = Field(
        description="Reference link to verify the source video or article"
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
    ideas: list[ContentIdea] = Field(description="List of 8-12 curated content ideas")


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
