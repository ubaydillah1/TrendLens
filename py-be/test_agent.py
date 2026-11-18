from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from app.agents.graphs.research_graph import research_graph

# Sample mock input data
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
    "tech_news_raw": [
        {
            "source": "HackerNews",
            "topic": "SQLite in production: Why companies are ditching PostgreSQL for embedded databases",
            "url": "https://news.ycombinator.com/item?id=sample3",
        },
        {
            "source": "GitHub Trending",
            "topic": "Prompt caching in LLMs reduced latency and cost by 80%",
            "url": "https://github.com/sample4",
        },
    ],
}

print("🚀 Running TrendLens Agent...")
result = research_graph.invoke(sample_input)

print("\n🎯 Final Report Generated:")
import json

print(json.dumps(result["final_report"], indent=2))
