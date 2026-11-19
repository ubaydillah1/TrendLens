"""Research agent graph definition and compilation."""

from langgraph.graph import END, START, StateGraph

from app.agents.nodes.query_planner_node import query_planner_node
from app.agents.nodes.synthesis_node import synthesis_node
from app.agents.nodes.tech_fetch_node import tech_fetch_node
from app.agents.nodes.viral_fetch_node import viral_fetch_node
from app.agents.states.research_state import ResearchAgentState

# Define the research workflow graph
workflow = StateGraph(ResearchAgentState)

# Register planner, ingestion, and synthesis nodes
workflow.add_node("query_planner", query_planner_node)
workflow.add_node("fetch_tech_news", tech_fetch_node)
workflow.add_node("fetch_viral_trends", viral_fetch_node)
workflow.add_node("synthesis", synthesis_node)

# Flow:
# 1. Fetch live tech news from Hacker News to anchor research in real events
# 2. Query planner uses breaking news + creator persona to plan targeted YouTube searches
# 3. Viral fetcher queries YouTube for live discussions and hooks matching the planned angles
# 4. Synthesis node creates localized, actionable content ideas
workflow.add_edge(START, "fetch_tech_news")
workflow.add_edge("fetch_tech_news", "query_planner")
workflow.add_edge("query_planner", "fetch_viral_trends")
workflow.add_edge("fetch_viral_trends", "synthesis")
workflow.add_edge("synthesis", END)

research_graph = workflow.compile()
