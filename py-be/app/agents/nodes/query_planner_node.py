"""Node for dynamically generating targeted video search queries."""

import os
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.agents.states.research_state import ResearchAgentState
from app.core.config import settings
from app.schemas.research import SearchQueries

PLANNER_SYSTEM_PROMPT = """You are an expert Social Video Research Strategist.

Your mission is to analyze today's breaking technical news and developer discussions, and generate 3 targeted, high-performing YouTube search queries to discover how creators are framing, debating, or hooking these specific topics.

Generate 3 distinct search angles grounded in today's developments:
1. Debate / Contrarian Angle: A polarizing argument, architectural dispute, or hype vs. reality check triggered by today's news.
2. Pain Point / Reality Check: A cautionary tale, costly blunder, security pitfall, or friction point connected to these topics.
3. Tooling / Practical Shift: Hands-on adoption, benchmark comparison, or productivity shift relevant to these stories.

Guidelines:
- Each query must be concise, natural, and realistic for a YouTube search bar (3 to 6 words).
- Ground the queries directly in today's news and discussions while aligning with the creator's niche and positioning.
- Avoid generic search terms like "coding tutorial"; target high-intent engineering discussions.
"""

PLANNER_USER_PROMPT = """Plan 3 targeted search queries for today's video research:

Creator Niche:
{niche}

Creator Positioning & Persona:
{user_positioning}

Today's Breaking Tech News & Engineering Debates:
{news_context}
"""


def query_planner_node(state: ResearchAgentState) -> dict[str, Any]:
    """Generates targeted search queries grounded in live tech news using GPT-4o-mini.

    Args:
        state: Current graph state containing 'niche', 'user_positioning', and 'tech_news_raw'.

    Returns:
        Partial state dictionary updating 'search_queries'.
    """
    api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=api_key,
    )

    structured_llm = llm.with_structured_output(SearchQueries)

    news_items = state.get("tech_news_raw") or []
    if news_items:
        formatted_news = "\n".join(
            f"- {item.get('topic', '')} ({item.get('engagement_score', 0)} pts)"
            for item in news_items[:8]
        )
    else:
        formatted_news = "No live news available; formulate queries based on evergreen niche dynamics."

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", PLANNER_SYSTEM_PROMPT),
            ("user", PLANNER_USER_PROMPT),
        ]
    )

    chain = prompt | structured_llm

    result: SearchQueries = chain.invoke(
        {
            "niche": state["niche"],
            "user_positioning": state["user_positioning"],
            "news_context": formatted_news,
        }
    )

    return {"search_queries": result.queries}
