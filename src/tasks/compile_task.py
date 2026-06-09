"""Factory for the LuaLaTeX compilation task."""

from crewai import Agent, Task


def build_compile_task(
    agent: Agent, abstract_task: Task, figure_embed_task: Task
) -> Task:
    return Task(
        description=(
            "All chapter files, figures, and latex_output/main.tex are already"
            " written and valid. Do NOT rewrite main.tex.\n\n"
            "Your ONLY job: call lualatex_runner_tool once:\n"
            "  tex_file='latex_output/main.tex'\n"
            "  passes=3\n\n"
            "After the tool call succeeds, emit:\n"
            "  [CHECKPOINT] Compilation complete: N pages."
        ),
        expected_output=(
            "latex_output/main.pdf exists; lualatex exits 0; page count reported."
        ),
        agent=agent,
        context=[abstract_task, figure_embed_task],
    )
