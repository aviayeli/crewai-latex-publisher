"""One-shot runner for chapter 6 only — uses existing book_outline.json as context."""
import dotenv

dotenv.load_dotenv()

from pathlib import Path  # noqa: E402

from crewai import Crew, Process, Task  # noqa: E402

from src.agents.content_agent import build_content_agent  # noqa: E402
from src.tasks.content_task import CHAPTER_SPECS  # noqa: E402

OUTLINE = Path("latex_output/book_outline.json").read_text(encoding="utf-8")

ch_num, heb_title, eng_title, pages = CHAPTER_SPECS[5]  # index 5 = chapter 6

skill = (
    Path("skills") / "hebrew-academic-writing" / "SKILL.md"
).read_text(encoding="utf-8")
agent = build_content_agent(skill)

task = Task(
    description=(
        f"Book outline (for reference):\n{OUTLINE}\n\n"
        f"Write chapter {ch_num} ({eng_title}) in Hebrew."
        f" Start with \\chapter{{{heb_title}}}. Do NOT include \\begin{{document}}."
        " Use \\( \\) for inline math and \\begin{equation} for display math."
        f" Target {pages} pages of content."
        f" When the full LaTeX text is ready, call latex_writer_tool with"
        f" path='latex_output/chapters/ch{ch_num}.tex',"
        " content=<the complete LaTeX text you wrote>, mode='write'."
        " You MUST pass all three arguments together in a single tool call."
    ),
    expected_output=f"latex_output/chapters/ch{ch_num}.tex written.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print(result)
