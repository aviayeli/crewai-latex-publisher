"""Dedicated task: embed pre-generated figure assets into chapter files."""

from crewai import Agent, Task

_CH2_FIGURE = (
    "\\\\begin{figure}[htbp]\\n"
    "    \\\\centering\\n"
    "    \\\\includegraphics[width=0.85\\\\textwidth]"
    "{latex_output/assets/attention_complexity.png}\\n"
    "    \\\\caption{השוואת מורכבות חישובית: תשומת לב סטנדרטית"
    " \\\\textenglish{O(n\\\\textsuperscript{2})},"
    " לינארית \\\\textenglish{O(n \\\\log n)},"
    " ורקורנטי \\\\textenglish{O(n)}.}\\n"
    "    \\\\label{fig:attention_complexity}\\n"
    "\\\\end{figure}\\n"
)

_CH3_FIGURE = (
    "\\\\begin{figure}[htbp]\\n"
    "    \\\\centering\\n"
    "    \\\\input{figures/sdp_attention}\\n"
    "    \\\\caption{ארכיטקטורת \\\\textenglish{Scaled Dot-Product Attention}.}\\n"
    "    \\\\label{fig:sdp_attention}\\n"
    "\\\\end{figure}\\n"
)


def build_figure_embed_task(
    agent: Agent, figure_task: Task, bidi_task: Task
) -> Task:
    return Task(
        description=(
            "BiDi validation is complete. Figure assets already exist:"
            " latex_output/assets/attention_complexity.png"
            " and latex_output/figures/sdp_attention.tex.\n\n"
            "Make exactly TWO latex_writer_tool calls:\n\n"
            "CALL 1 — append \\\\includegraphics to ch2:\n"
            f"  path='chapters/ch2.tex', mode='append', content='{_CH2_FIGURE}'\n\n"
            "CALL 2 — append \\\\input{{figures/sdp_attention}} to ch3:\n"
            f"  path='chapters/ch3.tex', mode='append', content='{_CH3_FIGURE}'\n\n"
            "Do NOT regenerate or modify any other files."
            " After both calls emit:"
            " [CHECKPOINT] Figures embedded in ch2.tex and ch3.tex."
        ),
        expected_output=(
            "ch2.tex contains \\\\includegraphics{...attention_complexity.png};"
            " ch3.tex contains \\\\input{figures/sdp_attention}."
        ),
        agent=agent,
        context=[figure_task, bidi_task],
    )
