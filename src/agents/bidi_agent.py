from crewai import Agent

from src.config import settings
from src.tools.latex_writer import latex_writer_tool


def build_bidi_agent(backstory: str) -> Agent:
    return Agent(
        role="LaTeX BiDi Typesetting Specialist",
        goal=(
            "Validate and enforce BiDi correctness across all"
            " 6 chapter LaTeX files."
        ),
        backstory=backstory,
        tools=[latex_writer_tool],
        llm=settings.LLM_MODEL,
        max_retry_limit=settings.MAX_AGENT_RETRIES,
        verbose=True,
    )
