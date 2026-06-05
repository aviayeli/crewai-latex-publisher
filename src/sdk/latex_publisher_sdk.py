"""SDK entry point — the sole public interface between callers and the pipeline.

SDK-First Architecture contract:
  - CLI (src/cli.py), main.py, notebooks, and test harnesses call ONLY this class.
  - No external caller may import PublisherCrew directly.
  - The crew topology, agent wiring, and tool selection are internal details.
"""

from pathlib import Path

from src import __version__
from src.crew import PublisherCrew
from src.security.skill_sieve import skill_sieve

# Skills loaded progressively for every topic (always relevant for Hebrew LaTeX output)
_PROGRESSIVE_SKILLS = ("hebrew_nlp_expert", "latex_bidi_expert")


class LatexPublisherSDK:
    """Façade over the CrewAI publisher pipeline.

    The crew is created lazily on the first `run()` call and reused on
    subsequent calls within the same SDK instance, avoiding redundant agent
    initialisation overhead across interactive sessions.
    """

    def __init__(self) -> None:
        self._crew: PublisherCrew | None = None

    @property
    def version(self) -> str:
        """Package version, sourced from ``src.__version__``."""
        return __version__

    def _build_expert_context(self) -> str:
        """Load and SkillSieve-validate the progressive-disclosure expert skills.

        Skills in ``_PROGRESSIVE_SKILLS`` are always loaded for Hebrew LaTeX output.
        Content is bounded to 400 chars per skill to prevent context bloat.
        Missing skill files are silently skipped.
        """
        parts: list[str] = []
        for name in _PROGRESSIVE_SKILLS:
            path = Path("skills") / name / "SKILL.md"
            if path.exists():
                raw = path.read_text(encoding="utf-8")
                content = skill_sieve.validate_and_return(name, raw)
                parts.append(f"[{name}]\n{content[:400]}")
        return "\n\n".join(parts)

    def run(self, topic: str = "", research_focus: str = "") -> str:
        """Execute the full Markdown → PDF pipeline and return the crew output.

        Args:
            topic: The subject the agents will research and write about.
            research_focus: Progressive-disclosure context appended to the topic
                string before injection.  Guides the research agent toward a
                specific domain cluster (Deep Learning vs. Agent Architecture).

        Creates a new :class:`PublisherCrew` on the first call; reuses it
        on subsequent calls within the same SDK instance.
        """
        if self._crew is None:
            self._crew = PublisherCrew()
        enriched = (
            f"{topic}. Research focus: {research_focus}."
            if research_focus
            else topic
        )
        return self._crew.kickoff(inputs={
            "topic": enriched,
            "expert_context": self._build_expert_context(),
        })
