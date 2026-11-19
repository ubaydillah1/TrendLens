from dotenv import find_dotenv, load_dotenv
import json

load_dotenv(find_dotenv())

from app.agents.graphs.research_graph import research_graph

# Autonomous input: Niche and Positioning only!
sample_input = {
    "niche": "AI & Software Engineering",
    "user_positioning": "Pragmatic Senior Backend Engineer, skeptical of AI hype, focuses on real architecture and cost efficiency",
}

print("🚀 Running TrendLens Planner-Worker Agent Pipeline...")
result = research_graph.invoke(sample_input)

print("\n🧠 Dynamic Search Queries Planned by Agent:")
for idx, q in enumerate(result.get("search_queries", []), 1):
    print(f"  {idx}. \"{q}\"")

print("\n📹 Live YouTube Trends Ingested (Across Planned Queries):")
for item in result.get("viral_trends_raw", []):
    views = f"{item.get('views', 0):,}"
    print(f"  • [{item['platform']}] {item['title']} ({views} views) [Query: {item.get('discovered_via_query')}]")

print("\n📰 Live Tech News Ingested:")
for item in result.get("tech_news_raw", []):
    print(f"  • [{item['source']}] {item['topic']} ({item.get('engagement_score', 0)} pts)")

print("\n🎯 Final Cross-Synthesized Report Generated:")
print(json.dumps(result["final_report"], indent=2))
