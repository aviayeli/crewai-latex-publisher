from crewai import Agent

from src.config import settings
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
        llm=settings.LLM_MODEL,
        max_retry_limit=settings.MAX_AGENT_RETRIES,
        verbose=True,
    )
