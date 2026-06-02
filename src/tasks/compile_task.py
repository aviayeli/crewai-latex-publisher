from crewai import Agent, Task


def build_compile_task(
    agent: Agent, bidi_task: Task, figure_task: Task
) -> Task:
    return Task(
        description=(
            "Write latex_output/main.tex via latex_writer_tool."
            " Use \\documentclass[17pt,a4paper]{extarticle}."
            " Load packages: fontspec, polyglossia, biblatex, geometry,"
            " graphicx, amsmath, hyperref, tikz, booktabs, xcolor."
            " Set \\setmainlanguage{hebrew} and \\setotherlanguage{english}."
            " Hebrew font fallback: David CLM → Frank Ruehl CLM → Noto Serif Hebrew."
            " Add \\addbibresource{refs.bib}."
            " Include chapters/ch1 through chapters/ch6 via \\input{}."
            " Add \\printbibliography before \\end{document}."
            " Then call lualatex_runner_tool with tex_file='latex_output/main.tex'"
            " and passes=2."
        ),
        expected_output="latex_output/main.pdf exists; two-pass lualatex exits 0.",
        agent=agent,
        context=[bidi_task, figure_task],
    )
