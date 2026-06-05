"""Factory for the Perplexity research task."""

from crewai import Agent, Task


def build_research_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Use perplexity_search_tool to research at least 6 peer-reviewed sources"
            " on the topic: {topic}."
            " Then apply the two-folder wiki pattern:\n"
            " Step 1 — Save the raw Perplexity output verbatim to"
            " 'raw/research_raw.md' via latex_writer_tool"
            " (path='raw/research_raw.md', mode='write').\n"
            " Step 2 — Distill into concise wiki entries (one paragraph per source,"
            " citation key + one-sentence contribution) and save to"
            " 'wiki/sources.md' via latex_writer_tool"
            " (path='wiki/sources.md', mode='write').\n"
            " Step 3 — Write 'wiki/index.md' listing each citation key with a"
            " one-line description and a link to wiki/sources.md"
            " (path='wiki/index.md', mode='write').\n"
            " Return ONLY the distilled wiki/sources.md content as task output."
            " Do NOT return the raw Perplexity dump — that is for audit only."
        ),
        expected_output=(
            "Distilled wiki summary: at least 6 citation keys, each with"
            " a one-paragraph description. Raw data saved to raw/research_raw.md."
        ),
        agent=agent,
        context=[],
    )
