from crewai import Agent, Task


def build_research_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Use perplexity_search_tool to research at least 6 academic sources"
            " on Transformer architectures, attention mechanisms, and Hebrew NLP."
            " Return a Markdown block with one entry per source containing:"
            " citation key (pattern: author_year_keyword), authors, year, title,"
            " venue, and a 2-sentence summary."
        ),
        expected_output=(
            "Structured research notes with at least 6"
            " citation-ready academic sources."
        ),
        agent=agent,
        context=[],
    )
