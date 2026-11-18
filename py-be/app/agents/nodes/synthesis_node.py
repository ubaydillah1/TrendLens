import json
import os
from datetime import UTC, datetime
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agents.states.research_state import ResearchAgentState
from app.schemas.research import DailyResearchReport

SYNTHESIS_SYSTEM_PROMPT = """You are an elite Technical Content Strategist & Viral Creative Director.

Your mission is to perform "Cross-Synthesis":
1. Study the provided VIRAL TRENDS (their psychological hook formulas, formatting, and virality triggers).
2. Study the provided TECHNICAL NEWS/ISSUES (real engineering debates, updates, release notes, or bugs).
3. MARRY THEM: Take the viral hook formulas and adapt them to address the real technical issues.
4. STRICT ALIGNMENT: Everything must strictly reflect the user's specific positioning, tone, and brand persona.

Rules:
- Generate 8 to 12 distinct, high-performing content ideas.
- Categorize each into appropriate buckets (e.g., 'Debate / Hot Take', 'Utility Hack', 'Career Reality', 'Architecture Deep-Dive').
- Provide 2-3 punchy, spoken-word hook variations for the first 3 seconds of a short-form video.
- Outline 3-4 bullet points detailing the core content message.
- Include real or provided source reference URLs for verification.
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
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    # Using Gemini 3.5 Flash Lite for fast, resilient structured output generation
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
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
