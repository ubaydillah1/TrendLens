"""Node for dynamically generating targeted video search queries."""

import os
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.agents.states.research_state import ResearchAgentState
from app.schemas.research import SearchQueries

PLANNER_SYSTEM_PROMPT = """You are an expert Social Video Research Strategist.

Your mission is to generate 3 diverse, high-performing YouTube search queries tailored to discover trending video formats, discussions, and viral hooks for a creator's niche and positioning.

Create 3 distinct search angles:
1. Debate / Contrarian Angle: A polarizing topic, architectural argument, or sacred cow being questioned.
2. Pain Point / Cautionary Angle: A costly mistake, cloud bill shock, security blunder, or horror story.
3. Industry Shift / Utility Angle: A real-world tooling shift, benchmark, career reality, or productivity breakthrough.

Guidelines:
- Each query must be concise, natural, and realistic for a YouTube search bar (3 to 6 words).
- Avoid generic queries like "programming tutorials"; target high-intent discussions.
"""

PLANNER_USER_PROMPT = """Plan 3 diverse search queries for today's research:

Creator Niche:
{niche}

Creator Positioning & Persona:
{user_positioning}
"""


def query_planner_node(state: ResearchAgentState) -> dict[str, Any]:
    """Generates dynamic, angle-specific search queries using GPT-4o-mini.

    Args:
        state: Current graph state containing 'niche' and 'user_positioning'.

    Returns:
        Partial state dictionary updating 'search_queries'.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=api_key,
    )

    structured_llm = llm.with_structured_output(SearchQueries)

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
        }
    )

    return {"search_queries": result.queries}
