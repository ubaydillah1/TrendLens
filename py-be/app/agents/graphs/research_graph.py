"""Research agent graph definition and compilation."""

from langgraph.graph import END, StateGraph

from app.agents.nodes.synthesis_node import synthesis_node
from app.agents.nodes.tech_fetch_node import tech_fetch_node
from app.agents.states.research_state import ResearchAgentState

# Define the research workflow graph
workflow = StateGraph(ResearchAgentState)

# Register nodes
workflow.add_node("fetch_tech_news", tech_fetch_node)
workflow.add_node("synthesis", synthesis_node)

# Flow: START -> fetch_tech_news -> synthesis -> END
workflow.set_entry_point("fetch_tech_news")
workflow.add_edge("fetch_tech_news", "synthesis")
workflow.add_edge("synthesis", END)

research_graph = workflow.compile()
