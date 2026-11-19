import json
import os
from datetime import UTC, datetime
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.agents.states.research_state import ResearchAgentState
from app.core.config import settings
from app.schemas.research import DailyResearchReport

SYNTHESIS_SYSTEM_PROMPT = """You are an elite Technical Content Strategist & Viral Creative Director.

Your mission is to perform "Cross-Synthesis":
1. Study the provided VIRAL TRENDS (titles, views, and especially the 'transcript_hook' spoken opening dialog).
2. Study the provided TECHNICAL NEWS/ISSUES (breaking news, security advisories, release notes, and community debates).
3. MARRY THEM: Combine the viral hook formulas and cadence with the breaking technical issues.
4. STRICT ALIGNMENT: Everything must strictly reflect the user's specific positioning, tone, and brand persona.

STRICT DIVERSITY & QUALITY RULES:
- Generate EXACTLY 10 distinct, high-performing content ideas.
- MANDATORY 10-SOURCE DIVERSITY: Each of the 10 ideas MUST be anchored to a COMPLETELY DIFFERENT story from 'tech_news_raw'. You are strictly forbidden from creating multiple ideas on the same subject (e.g., maximum 1 idea for NGINX, maximum 1 idea for Gemini, maximum 1 idea for Deutsche Bank, maximum 1 idea for Codeberg, etc.). Select 10 different stories from the 20+ stories provided!
- TRIPLE REFERENCE PACK: Every idea MUST include:
  * news_source_url: direct article or release URL from the chosen story
  * community_discussion_url: discussion/comments URL (Hacker News or Lobsters) from the chosen story
  * inspiration_video_url: reference YouTube video URL from 'viral_trends_raw'
- SHORT-FORM PRODUCTION CUES:
  * visual_hook_direction: specific visual action for seconds 0-3 (e.g., screen recording terminal, highlighting CVE docs, showing cost graphs).
  * technical_datapoint: include a specific metric, CVE code, benchmark latency, or hard figure.
  * engagement_cta: spoken closing question designed to spark arguments or sharing in the comments section.
- Categorize each idea into appropriate buckets ('Debate / Hot Take', 'Utility Hack', 'Career Reality', 'Architecture Deep-Dive').

Language & Localization Standards:
- The content (topic_title, viral_hooks, visual_hook_direction, content_outline, engagement_cta, why_it_works) MUST be written in natural, conversational, modern Indonesian (Bahasa Indonesia yang santai, lugas, dan persuasif untuk kreator tech).
- Spoken hooks and CTA must sound natural when spoken aloud on camera (e.g., "Lu kira...", "Stop buang-buang...", "Kenapa banyak yang nyesel...").
- Keep standard software engineering terminology in original English (e.g., 'Nginx', 'RCE', 'cloud bills', 'microservices', 'prompt caching', 'monolith', 'Docker', 'latency', 'benchmark').
"""

SYNTHESIS_USER_PROMPT = """Generate today's content research report with the following context:

Target Niche:
{niche}

User Positioning & Persona:
{user_positioning}

Recent Viral Trends & Hook Formats (YouTube / Instagram):
{viral_trends_raw}

Current Technical News & Engineering Issues:
{tech_news_raw}
"""


def synthesis_node(state: ResearchAgentState) -> dict[str, Any]:
    """Synthesizes raw viral trends and technical news into structured content ideas.

    Marries social media hook patterns with engineering news, filtering the output
    through the creator's specific brand positioning.

    Args:
        state: Graph state containing raw trends, news, niche, and user positioning.

    Returns:
        Partial state dictionary updating 'final_report' with the validated payload.
    """
    api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")

    # Using GPT-4o-mini for reliable, low-cost structured synthesis
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=api_key,
    )

    structured_llm = llm.with_structured_output(DailyResearchReport)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYNTHESIS_SYSTEM_PROMPT),
            ("user", SYNTHESIS_USER_PROMPT),
        ]
    )

    chain = prompt | structured_llm

    # Serialize raw inputs into formatted JSON strings for template interpolation
    report: DailyResearchReport = chain.invoke(
        {
            "niche": state["niche"],
            "user_positioning": state["user_positioning"],
            "viral_trends_raw": json.dumps(state.get("viral_trends_raw", []), indent=2),
            "tech_news_raw": json.dumps(state.get("tech_news_raw", []), indent=2),
        }
    )

    # Ensure UTC timestamp is always populated if omitted by the model
    if not report.date:
        report.date = datetime.now(UTC).isoformat()

    return {"final_report": report.model_dump()}
