"""SDK entry point — the sole public interface between callers and the pipeline.

SDK-First Architecture contract:
  - CLI (src/cli.py), main.py, notebooks, and test harnesses call ONLY this class.
  - No external caller may import PublisherCrew directly.
  - The crew topology, agent wiring, and tool selection are internal details.
"""

from src import __version__
from src.crew import PublisherCrew


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

    def run(self) -> str:
        """Execute the full Markdown → PDF pipeline and return the crew output.

        Creates a new :class:`PublisherCrew` on the first call; reuses it
        on subsequent calls within the same SDK instance.
        """
        if self._crew is None:
            self._crew = PublisherCrew()
        return self._crew.kickoff()
