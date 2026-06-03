"""Factory for the Academic Outline Architect agent."""

from crewai import Agent

from src.config import build_llm, settings
from src.tools.latex_writer import latex_writer_tool


def build_outline_agent(backstory: str) -> Agent:
    return Agent(
        role="Academic Outline Architect",
        goal=(
            "Produce a structured 6-chapter book outline as a"
            " valid JSON file at latex_output/book_outline.json."
        ),
        backstory=backstory,
        tools=[latex_writer_tool],
        llm=build_llm(),
        max_iter=settings.MAX_ITER,
        max_retry_limit=settings.MAX_AGENT_RETRIES,
        verbose=True,
    )
