import json
import os
from datetime import UTC, datetime
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.agents.states.research_state import ResearchAgentState
from app.schemas.research import DailyResearchReport

SYNTHESIS_SYSTEM_PROMPT = """You are an elite Technical Content Strategist & Viral Creative Director.

Your mission is to perform "Cross-Synthesis":
1. Study the provided VIRAL TRENDS (their titles, views, and especially the 'transcript_hook' spoken opening dialog when available).
2. Study the provided TECHNICAL NEWS/ISSUES (real engineering debates, updates, release notes, or bugs).
3. MARRY THEM: Take the viral hook formulas and spoken delivery styles, and adapt them to address the real technical issues.
4. STRICT ALIGNMENT: Everything must strictly reflect the user's specific positioning, tone, and brand persona.

Rules:
- Generate 8 to 12 distinct, high-performing content ideas.
- Categorize each into appropriate buckets (e.g., 'Debate / Hot Take', 'Utility Hack', 'Career Reality', 'Architecture Deep-Dive').
- Provide 2-3 punchy, spoken-word hook variations for the first 3 seconds of a short-form video.
- Outline 3-4 bullet points detailing the core content message.
- Include real or provided source reference URLs for verification.
- When 'transcript_hook' is available in viral trends, study the opening cadence, question pacing, and psychological triggers to craft realistic, high-retention spoken hooks.

Language & Localization Standards:
- The final output (topic_title, viral_hooks, content_outline, why_it_works) MUST be written in natural, conversational, modern Indonesian (Bahasa Indonesia yang santai, lugas, dan persuasif untuk kreator tech).
- The hooks must sound natural when spoken aloud on camera (e.g., "Lu kira...", "Stop buang-buang...", "Kenapa banyak yang nyesel...").
- Keep standard software engineering terminology in original English (e.g., 'Nginx', 'RCE', 'cloud bills', 'microservices', 'prompt caching', 'monolith', 'Docker', 'latency').
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
    api_key = os.getenv("OPENAI_API_KEY") 

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
