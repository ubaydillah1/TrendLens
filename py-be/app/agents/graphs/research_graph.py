"""Research agent graph definition and compilation."""

from langgraph.graph import END, StateGraph

from app.agents.nodes.synthesis_node import synthesis_node
from app.agents.states.research_state import ResearchAgentState

# Define the research workflow graph
workflow = StateGraph(ResearchAgentState)

workflow.add_node("synthesis", synthesis_node)
workflow.set_entry_point("synthesis")
workflow.add_edge("synthesis", END)

research_graph = workflow.compile()

