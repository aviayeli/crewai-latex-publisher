"""Factory for the BiDi Typesetting Specialist agent."""

from crewai import Agent

from src.config import build_llm_smart, settings
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
        llm=build_llm_smart(),
        max_iter=settings.MAX_ITER,
        max_retry_limit=settings.MAX_AGENT_RETRIES,
        verbose=True,
    )
