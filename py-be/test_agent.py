import json

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from app.agents.graphs.research_graph import research_graph

# Input without tech_news_raw: the agent fetches live news automatically!
sample_input = {
    "niche": "AI & Software Engineering",
    "user_positioning": "Pragmatic Senior Backend Engineer, skeptical of AI hype, focuses on real architecture and cost efficiency",
    "viral_trends_raw": [
        {
            "platform": "YouTube",
            "title": "Why Senior Devs Are Abandoning Microservices in 2026",
            "views": 450000,
            "hook_formula": "Contrarian / Exposing an industry regret",
            "source_url": "https://youtube.com/watch?v=sample1",
        },
        {
            "platform": "Instagram",
            "title": "3 Mistakes that Cost Startups $50k in Cloud Bills",
            "views": 210000,
            "hook_formula": "Direct financial pain point / Warning hook",
            "source_url": "https://instagram.com/reel/sample2",
        },
    ],
}

print("🚀 Running TrendLens Agent with LIVE Hacker News Ingestion...")
result = research_graph.invoke(sample_input)

print("\n📰 Live Tech News Ingested by Agent:")
for item in result.get("tech_news_raw", []):
    print(f"  • [{item['source']}] {item['topic']} ({item.get('engagement_score', 0)} pts)")

print("\n🎯 Final Cross-Synthesized Report Generated:")
print(json.dumps(result["final_report"], indent=2))
