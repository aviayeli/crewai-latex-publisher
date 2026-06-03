"""Factory for the BiDi validation task."""

from crewai import Agent, Task


def build_bidi_task(agent: Agent, content_tasks: list[Task]) -> Task:
    return Task(
        description=(
            "Read and validate all six chapter files in latex_output/chapters/."
            " Ensure ch3.tex contains: (1) an RTL paragraph with \\textenglish{},"
            " (2) a \\begin{equation} environment,"
            " (3) a \\begin{LTR}...\\end{LTR} block."
            " Overwrite each file in-place via latex_writer_tool if corrections"
            " are needed. Validate all 5 checklist items from the lualatex-bidi skill."
        ),
        expected_output=(
            "All six chapters updated in-place;"
            " ch3.tex contains all three mandatory BiDi constructs."
        ),
        agent=agent,
        context=content_tasks,
    )
