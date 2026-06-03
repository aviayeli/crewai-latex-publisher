"""Factory for the Academic Researcher agent."""

from crewai import Agent

from src.config import build_llm, settings
from src.tools.latex_writer import latex_writer_tool
from src.tools.perplexity_search import perplexity_search_tool


def build_researcher_agent(backstory: str) -> Agent:
    return Agent(
        role="Academic Researcher",
        goal=(
            "Use Perplexity AI to gather academic sources on"
            " Transformer architectures, then distill findings into wiki/."
        ),
        backstory=backstory,
        tools=[perplexity_search_tool, latex_writer_tool],
        llm=build_llm(),
        max_iter=settings.MAX_ITER,
        max_retry_limit=settings.MAX_AGENT_RETRIES,
        verbose=True,
    )
