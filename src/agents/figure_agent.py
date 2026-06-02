from crewai import Agent

from src.config import settings
from src.tools.latex_writer import latex_writer_tool
from src.tools.python_runner import python_runner_tool


def build_figure_agent(backstory: str) -> Agent:
    return Agent(
        role="Scientific Figure Generator",
        goal=(
            "Produce the attention complexity PNG and the"
            " TikZ scaled dot-product attention diagram."
        ),
        backstory=backstory,
        tools=[python_runner_tool, latex_writer_tool],
        llm=settings.LLM_MODEL,
        max_retry_limit=settings.MAX_AGENT_RETRIES,
        verbose=True,
    )
