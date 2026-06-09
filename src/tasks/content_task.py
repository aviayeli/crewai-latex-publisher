"""Factory for per-chapter content writing tasks (markdown-first workflow)."""

from crewai import Agent, Task

CHAPTER_SPECS: list[tuple[int, str, str, int]] = [
    (1, "מבוא", "Introduction to Transformers", 2),
    (2, "ארכיטקטורה", "Transformer Architecture Deep Dive", 3),
    (3, "לולאות חשיבה-פעולה", "Reasoning-Action Loops and Chain-of-Thought", 2),
    (4, "יישומים", "Applications and Fine-Tuning", 3),
    (5, "הערכה", "Evaluation Methodologies", 2),
    (6, "סיכום", "Conclusion and Future Work", 3),
]
assert sum(pages for _, _, _, pages in CHAPTER_SPECS) == 15

_MD_PATH = "chapters/ch{n}.md"
_TEX_PATH = "chapters/ch{n}.tex"


def build_content_tasks(
    agent: Agent, outline_task: Task, research_task: Task
) -> list[Task]:
    tasks = []
    for ch_num, heb_title, eng_title, pages in CHAPTER_SPECS:
        md = _MD_PATH.format(n=ch_num)
        tex = _TEX_PATH.format(n=ch_num)
        first_chunk = (
            f"content='\\\\chapter{{{heb_title}}}\\n\\n"
            f"\\\\section{{<first section>}}\\n<prose>'"
        )
        desc = (
            f"Write chapter {ch_num} ({eng_title}) in Hebrew"
            " using markdown-first workflow.\n"
            "Use wiki/sources.md from research context for citations"
            " — do NOT re-fetch.\n\n"
            f"STEP 1 — Write '{md}' section by section via latex_writer_tool:\n"
            f"  First call: path='{md}', mode='write', {first_chunk}\n"
            f"  Each additional section: path='{md}', mode='append',"
            " content='\\n\\\\section{<heading>}\\n<prose>'\n"
            "  Inline LaTeX commands (\\\\textenglish{}, \\\\cite{},"
            " \\\\begin{equation}) must be embedded in the markdown.\n\n"
            f"STEP 2 — Convert: markdown_converter_tool"
            f"(md_path='{md}', tex_path='{tex}').\n\n"
            "CHECKPOINT after step 1: report sections written and word count.\n"
            f"CHECKPOINT after step 2: report whether '{tex}' was created.\n"
            f"Target {pages} pages (~{pages * 375} words)."
            " Do NOT include \\\\begin{document}."
        )
        tasks.append(
            Task(
                description=desc,
                expected_output=(
                    f"'{tex}' written. Estimated pages: {pages}."
                    " Both checkpoints reported."
                ),
                agent=agent,
                context=[outline_task, research_task],
            )
        )
    return tasks
