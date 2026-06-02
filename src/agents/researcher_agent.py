from crewai import Agent

from src.config import settings
from src.tools.perplexity_search import perplexity_search_tool


def build_researcher_agent(backstory: str) -> Agent:
    return Agent(
        role="Academic Researcher",
        goal=(
            "Use Perplexity AI to gather academic sources on"
            " Transformer architectures for the outline agent."
        ),
        backstory=backstory,
        tools=[perplexity_search_tool],
        llm=settings.LLM_MODEL,
        max_retry_limit=settings.MAX_AGENT_RETRIES,
        verbose=True,
    )
