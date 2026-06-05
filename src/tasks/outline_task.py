"""Factory for the book outline task."""

from crewai import Agent, Task


def build_outline_task(agent: Agent, research_task: Task) -> Task:
    return Task(
        description=(
            "Using the research notes on {topic}, write a valid JSON file to"
            " latex_output/book_outline.json via latex_writer_tool."
            " The JSON must include fields: title, subtitle, and a chapters"
            " array with number, hebrew_title, english_title, page_budget,"
            " and sections. All 6 chapter page_budget values must sum to 15."
            " The file path must be exactly latex_output/book_outline.json."
        ),
        expected_output=(
            "Valid JSON file at latex_output/book_outline.json with 6 chapters."
        ),
        agent=agent,
        context=[research_task],
    )
