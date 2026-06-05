"""SDK entry-point: assembles agents, tasks, and the Crew for the publisher pipeline."""

from pathlib import Path

from crewai import Crew, Process

from src.agents.bidi_agent import build_bidi_agent
from src.agents.compiler_agent import build_compiler_agent
from src.agents.content_agent import build_content_agent
from src.agents.figure_agent import build_figure_agent
from src.agents.manager_agent import build_manager_agent
from src.agents.outline_agent import build_outline_agent
from src.agents.researcher_agent import build_researcher_agent
from src.security.skill_sieve import skill_sieve
from src.tasks.bidi_task import build_bidi_task
from src.tasks.compile_task import build_compile_task
from src.tasks.content_task import build_content_tasks
from src.tasks.figure_task import build_figure_task
from src.tasks.outline_task import build_outline_task
from src.tasks.research_task import build_research_task


def _load_skill(name: str) -> str:
    content = (Path("skills") / name / "SKILL.md").read_text(encoding="utf-8")
    return skill_sieve.validate_and_return(name, content)


class PublisherCrew:
    def __init__(self, topic: str = "") -> None:
        mgr_skill = _load_skill("manager")
        res_skill = _load_skill("perplexity-research")
        out_skill = _load_skill("academic-outline")
        con_skill = _load_skill("hebrew-academic-writing")
        bdi_skill = _load_skill("lualatex-bidi")
        fig_skill = _load_skill("matplotlib-tikz")
        cmp_skill = _load_skill("lualatex-build")
        lat_skill = _load_skill("latex_expert")

        self.manager_agent = build_manager_agent(mgr_skill)
        self.researcher_agent = build_researcher_agent(res_skill)
        self.outline_agent = build_outline_agent(out_skill)
        self.content_agent = build_content_agent(con_skill)
        self.bidi_agent = build_bidi_agent(bdi_skill)
        self.figure_agent = build_figure_agent(fig_skill)
        self.compiler_agent = build_compiler_agent(cmp_skill + "\n\n" + lat_skill)

        self.research_task = build_research_task(self.researcher_agent, topic)
        self.outline_task = build_outline_task(
            self.outline_agent, self.research_task, topic
        )
        self.content_tasks = build_content_tasks(
            self.content_agent, self.outline_task, self.research_task
        )
        self.figure_task = build_figure_task(
            self.figure_agent, self.outline_task
        )
        self.bidi_task = build_bidi_task(self.bidi_agent, self.content_tasks)
        self.compile_task = build_compile_task(
            self.compiler_agent, self.bidi_task, self.figure_task
        )

    def kickoff(self) -> str:
        tasks = [
            self.research_task,
            self.outline_task,
            *self.content_tasks,
            self.figure_task,
            self.bidi_task,
            self.compile_task,
        ]
        crew = Crew(
            manager_agent=self.manager_agent,
            agents=[
                self.researcher_agent,
                self.outline_agent,
                self.content_agent,
                self.bidi_agent,
                self.figure_agent,
                self.compiler_agent,
            ],
            tasks=tasks,
            process=Process.hierarchical,
            verbose=True,
        )
        return crew.kickoff()
