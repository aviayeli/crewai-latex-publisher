"""Reusable mixin classes for cross-cutting concerns."""


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
