"""Reusable mixin classes for cross-cutting concerns."""


class MemoryManagerMixin:
    """Mixin that implements the Compact pattern for context-window management.

    Solves the "Lost in the Middle" phenomenon by summarising older sections
    and keeping only an executive summary + the active working window in the
    agent's live context.
    """

    def compact(self, sections: list[str]) -> str:
        """Summarise *sections* into a single executive-summary string.

        Deterministic — no LLM call.  Produces a bullet list of section
        headings (first 60 chars) plus total word count so downstream agents
        know what was compacted without re-reading the full text.
        """
        if not sections:
            return ""
        total_words = sum(len(s.split()) for s in sections)
        bullets = "\n".join(
            f"  • {s[:60].split(chr(10))[0].strip()}" for s in sections
        )
        return (
            f"[COMPACT SUMMARY — {len(sections)} section(s), ~{total_words} words]\n"
            f"{bullets}"
        )

    def active_context(self, full_history: list[str], window: int = 3) -> list[str]:
        """Return executive summary of older sections + the last *window* items.

        If ``len(full_history) <= window`` the list is returned unchanged.
        """
        if len(full_history) <= window:
            return list(full_history)
        older = full_history[:-window]
        recent = full_history[-window:]
        return [self.compact(older)] + list(recent)


class FinOpsMixin:
    """Mixin that adds per-instance LLM token and call-count tracking.

    Subclasses must call ``_init_finops()`` in their ``__init__``.
    """

    def _init_finops(self) -> None:
        self._prompt_tokens: int = 0
        self._completion_tokens: int = 0
        self._call_count: int = 0

    def record_tokens(self, prompt_tokens: int, completion_tokens: int) -> None:
        """Accumulate token counts and increment the call counter."""
        self._prompt_tokens += prompt_tokens
        self._completion_tokens += completion_tokens
        self._call_count += 1

    @property
    def total_tokens(self) -> int:
        return self._prompt_tokens + self._completion_tokens

    @property
    def call_count(self) -> int:
        return self._call_count

    def reset_finops(self) -> None:
        """Reset all counters to zero."""
        self._prompt_tokens = 0
        self._completion_tokens = 0
        self._call_count = 0
