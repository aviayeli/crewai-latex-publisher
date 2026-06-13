"""ApiGatekeeper — governs all external LLM/API factory calls.

Every call to build_llm*, build_llm_fast, or build_llm_smart is routed
through ``ApiGatekeeper.guard()``, which enforces a per-minute rate limit
and records each call in the FinOps ledger.
"""
import threading
import time
from collections.abc import Callable
from typing import Any

from src.utils.mixins import FinOpsMixin


class RateLimitExceededError(RuntimeError):
    """Raised when the configured calls-per-minute cap is exceeded."""


class ApiGatekeeper(FinOpsMixin):
    """Centralised gateway for all external LLM and API calls.

    Inherits :class:`FinOpsMixin` to satisfy the V3 mixin OOP requirement.
    """

    def __init__(self, calls_per_minute: int = 60) -> None:
        self._init_finops()
        self._calls_per_minute = calls_per_minute
        self._window_start: float = time.monotonic()
        self._window_calls: int = 0
        self._lock = threading.Lock()

    def _check_rate_limit(self) -> None:
        now = time.monotonic()
        with self._lock:
            if now - self._window_start >= 60.0:
                self._window_start = now
                self._window_calls = 0
            if self._window_calls >= self._calls_per_minute:
                raise RateLimitExceededError(
                    f"Rate limit of {self._calls_per_minute} calls/min exceeded"
                )
            self._window_calls += 1

    def guard(self, factory_fn: Callable[[], Any]) -> Any:
        """Enforce rate limit then invoke *factory_fn*, returning its result."""
        self._check_rate_limit()
        result = factory_fn()
        self.record_tokens(0, 0)  # register the guarded call in the FinOps ledger
        return result
