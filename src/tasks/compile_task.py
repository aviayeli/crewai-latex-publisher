"""Factory for the LuaLaTeX compilation task."""

from crewai import Agent, Task


def build_compile_task(
    agent: Agent, bidi_task: Task, figure_task: Task
) -> Task:
    return Task(
        description=(
            "Write latex_output/main.tex via latex_writer_tool."
            " Use \\documentclass[17pt,a4paper]{extarticle}."
            " Load packages: fontspec, polyglossia, biblatex, geometry,"
            " graphicx, amsmath, hyperref, tikz, booktabs, xcolor, float."
            " Set \\setmainlanguage{hebrew} and \\setotherlanguage{english}."
            " Hebrew font fallback: David CLM → Frank Ruehl CLM → Noto Serif Hebrew."
            " Add \\addbibresource{refs.bib}."
            " MANDATORY cover page metadata — these three lines are REQUIRED"
            " and must appear in the preamble before \\begin{document}:\n"
            "   \\title{ארכיטקטורת הטרנספורמר ועיבוד שפה טבעית בעברית}\n"
            "   \\author{Avi Ayeli -- 300228160}\n"
            "   \\date{\\textenglish{June 2026}}\n"
            " After \\begin{document}, the FIRST THREE commands must be"
            " \\maketitle, \\tableofcontents, \\newpage — in that order."
            " Then include chapters/ch1 through chapters/ch6 via \\input{}."
            " Add \\printbibliography before \\end{document}."
            " Then call lualatex_runner_tool with tex_file='latex_output/main.tex'"
            " and passes=2."
        ),
        expected_output=(
            "latex_output/main.pdf exists; two-pass lualatex exits 0."
            " Cover page shows author 'Avi Ayeli -- 300228160' and date 'June 2026'."
        ),
        agent=agent,
        context=[bidi_task, figure_task],
    )
