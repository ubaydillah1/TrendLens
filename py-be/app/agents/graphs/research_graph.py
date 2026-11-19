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

# Flow: START -> query_planner
workflow.add_edge(START, "query_planner")

# Parallel Fan-Out from query_planner:
# 1. Fetch viral YouTube trends using dynamically planned search queries
# 2. Concurrently fetch high-engagement Hacker News engineering debates
workflow.add_edge("query_planner", "fetch_viral_trends")
workflow.add_edge("query_planner", "fetch_tech_news")

# Fan-In: Both ingestion streams must complete before synthesis begins
workflow.add_edge("fetch_tech_news", "synthesis")
workflow.add_edge("fetch_viral_trends", "synthesis")

# Terminate workflow upon completing synthesis
workflow.add_edge("synthesis", END)

research_graph = workflow.compile()
