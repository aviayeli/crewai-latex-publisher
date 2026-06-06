"""Factory for the BiDi validation task."""

from crewai import Agent, Task


def build_bidi_task(agent: Agent, content_tasks: list[Task]) -> Task:
    return Task(
        description=(
            "Read and validate all six chapter files in latex_output/chapters/."
            " Ensure ch3.tex contains: (1) an RTL paragraph with \\textenglish{},"
            " (2) a \\begin{equation} environment,"
            " (3) a \\begin{LTR}...\\end{LTR} block."
            " MANDATORY FIGURE — at least one chapter must embed the complexity plot:"
            " a \\begin{figure}[htbp]...\\end{figure} block containing"
            " \\includegraphics[width=0.85\\textwidth]"
            "{latex_output/assets/attention_complexity.png}."
            " If missing, insert it into ch2.tex after its first \\section{}."
            " MANDATORY TABLE — at least one chapter must contain a"
            " \\begin{table}[htbp]...\\end{table} block with a model comparison"
            " (columns: Model, Parameters, BLEU/Accuracy, Notes)."
            " If missing, insert it into ch4.tex after its first \\section{}."
            " Overwrite each file in-place via latex_writer_tool if corrections"
            " are needed. Validate all checklist items from the lualatex-bidi skill."
        ),
        expected_output=(
            "All six chapters updated in-place;"
            " ch3.tex contains all three mandatory BiDi constructs;"
            " at least one chapter contains \\includegraphics"
            " for attention_complexity.png;"
            " at least one chapter contains \\begin{table} model comparison."
        ),
        agent=agent,
        context=content_tasks,
    )
