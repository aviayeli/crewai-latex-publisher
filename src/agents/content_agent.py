from crewai import Agent

from src.config import settings
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
        llm=settings.LLM_MODEL,
        max_retry_limit=settings.MAX_AGENT_RETRIES,
        verbose=True,
    )
