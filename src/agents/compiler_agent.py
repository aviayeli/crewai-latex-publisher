"""Factory for the LaTeX Build Engineer agent."""

from crewai import Agent

from src.config import build_llm_fast, settings
from src.tools.lualatex_runner import lualatex_runner_tool


def build_compiler_agent(backstory: str) -> Agent:
    return Agent(
        role="LaTeX Build Engineer",
        goal=(
            "Assemble main.tex preamble and run two-pass"
            " lualatex compilation to produce main.pdf."
        ),
        backstory=backstory,
        tools=[lualatex_runner_tool],
        llm=build_llm_fast(),
        max_iter=settings.MAX_ITER,
        max_retry_limit=settings.MAX_AGENT_RETRIES,
        verbose=True,
    )
