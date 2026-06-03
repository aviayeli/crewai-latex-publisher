"""Factory for the Project Manager (orchestrator) agent."""

from crewai import Agent

from src.config import build_llm, settings


def build_manager_agent(backstory: str) -> Agent:
    return Agent(
        role="Project Manager",
        goal=(
            "Orchestrate all sub-agents to produce a compiled"
            " Hebrew academic PDF."
        ),
        backstory=backstory,
        allow_delegation=True,
        llm=build_llm(),
        max_iter=settings.MAX_ITER,
        max_retry_limit=settings.MAX_AGENT_RETRIES,
        verbose=True,
        tools=[],
    )
