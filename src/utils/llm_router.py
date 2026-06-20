"""LLMRouter — FinOps-aware routing between heavy API and local LLM.

Complex tasks (structuring, reasoning) are dispatched to the Anthropic API
via ``build_llm_smart``.  Simple, repetitive tasks (formatting, syntax fixes)
are served by ``LocalLLMStub``, which simulates an Ollama/local integration
to avoid burning cloud budget on mechanical work.

When ``settings.DRY_RUN`` is True the router always returns the cheapest
available LLM (``build_llm_fast``) with ``max_tokens=10``, allowing a full
pipeline smoke-test without meaningful API spend.
"""
from __future__ import annotations

from enum import Enum
from typing import Any

from src.config import build_llm_fast, build_llm_smart, settings
from src.utils.mixins import FinOpsMixin


class TaskComplexity(Enum):
    """Complexity tier used to select the appropriate LLM backend."""

    SIMPLE = "simple"
    COMPLEX = "complex"


class LocalLLMStub:
    """Simulated Ollama/local LLM connection for simple formatting tasks.

    In production this would wrap an ``ollama`` client or a local OpenAI-
    compatible endpoint.  As a stub it carries only the model identifier so
    tests and config validation can inspect it without network calls.
    """

    def __init__(self, model: str = "ollama/llama3") -> None:
        self.model = model

    def __repr__(self) -> str:
        return f"LocalLLMStub(model={self.model!r})"


_SIMPLE_KEYWORDS: frozenset[str] = frozenset(
    {"format", "fix", "spell", "syntax", "indent", "lint"}
)


class LLMRouter(FinOpsMixin):
    """Routes incoming tasks to the appropriate LLM backend.

    Inherits :class:`FinOpsMixin` so every routing decision is recorded in
    the FinOps ledger and observable via ``call_count`` / ``total_tokens``.
    """

    def __init__(self) -> None:
        self._init_finops()

    def route(self, complexity: TaskComplexity) -> Any:
        """Return the LLM (or stub) appropriate for *complexity*.

        DRY_RUN overrides all routing: returns ``build_llm_fast()`` so the
        pipeline compiles end-to-end with negligible token spend.
        """
        self.record_tokens(0, 0)
        if settings.DRY_RUN:
            return build_llm_fast()
        if complexity == TaskComplexity.COMPLEX:
            return build_llm_smart()
        return LocalLLMStub()

    def classify(self, task_description: str) -> TaskComplexity:
        """Heuristic: classify a task description as SIMPLE or COMPLEX.

        If the description contains any simple-task keyword (format, fix,
        spell, syntax, indent, lint) it is SIMPLE; otherwise COMPLEX.
        """
        desc_lower = task_description.lower()
        if any(kw in desc_lower for kw in _SIMPLE_KEYWORDS):
            return TaskComplexity.SIMPLE
        return TaskComplexity.COMPLEX
