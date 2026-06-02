from crewai import Agent, Task

CHAPTER_SPECS: list[tuple[int, str, str, int]] = [
    (1, "מבוא", "Introduction to Transformers", 2),
    (2, "ארכיטקטורה", "Transformer Architecture Deep Dive", 3),
    (3, "דו-כיווניות", "BiDi Text in Academic Publishing", 2),
    (4, "יישומים", "Applications and Fine-Tuning", 3),
    (5, "הערכה", "Evaluation Methodologies", 2),
    (6, "סיכום", "Conclusion and Future Work", 3),
]
assert sum(pages for _, _, _, pages in CHAPTER_SPECS) == 15


def build_content_tasks(agent: Agent, outline_task: Task) -> list[Task]:
    tasks = []
    for ch_num, heb_title, eng_title, pages in CHAPTER_SPECS:
        desc = (
            f"Write chapter {ch_num} ({eng_title}) in Hebrew."
            f" Save to latex_output/chapters/ch{ch_num}.tex via latex_writer_tool."
            f" Start with \\chapter{{{heb_title}}}. Do NOT include \\begin{{document}}."
            " Use \\( \\) for inline math and \\begin{equation} for display math."
            f" Target {pages} pages."
        )
        tasks.append(
            Task(
                description=desc,
                expected_output=f"latex_output/chapters/ch{ch_num}.tex written.",
                agent=agent,
                context=[outline_task],
            )
        )
    return tasks
