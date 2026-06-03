"""Factory for the Hebrew Academic Writer agent."""

from crewai import Agent

from src.config import build_llm, settings
from src.tools.latex_writer import latex_writer_tool
from src.tools.markdown_converter import markdown_converter_tool


def build_content_agent(backstory: str) -> Agent:
    return Agent(
        role="Hebrew Academic Writer",
        goal=(
            "Write Hebrew academic chapter files using the"
            " Markdown-first workflow: write .md then convert to .tex."
        ),
        backstory=backstory,
        tools=[latex_writer_tool, markdown_converter_tool],
        llm=build_llm(),
        max_iter=settings.MAX_ITER,
        max_retry_limit=settings.MAX_AGENT_RETRIES,
        verbose=True,
    )
