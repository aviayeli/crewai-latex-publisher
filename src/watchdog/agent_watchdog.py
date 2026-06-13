"""Watchdog wrapper: kills hanging agents after WATCHDOG_TIMEOUT seconds."""
from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from src.config import settings

_TRACE_LOG = Path("logs/agent_trace.log")
_TRACE_LOG.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(_TRACE_LOG),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
_log = logging.getLogger("watchdog")

TIMEOUT_SECONDS: int = getattr(settings, "WATCHDOG_TIMEOUT", 300)


class WatchdogTimeoutError(RuntimeError):
    pass


def _run_with_timeout(fn: Callable, args: tuple, kwargs: dict,
                      timeout: int) -> Any:
    result: list[Any] = []
    exc: list[BaseException] = []

    def _target():
        try:
            result.append(fn(*args, **kwargs))
        except Exception as e:  # noqa: BLE001
            exc.append(e)

    fn_name = getattr(fn, '__qualname__', None) or getattr(fn, '__name__', repr(fn))
    thread = threading.Thread(target=_target, daemon=True)
    _log.info("AGENT_START fn=%s timeout=%ds", fn_name, timeout)
    t0 = time.monotonic()
    thread.start()
    thread.join(timeout=timeout)

    elapsed = time.monotonic() - t0
    if thread.is_alive():
        _log.error("AGENT_TIMEOUT fn=%s elapsed=%.1fs", fn_name, elapsed)
        raise WatchdogTimeoutError(
            f"{fn_name} exceeded {timeout}s timeout."
        )

    if exc:
        _log.error("AGENT_ERROR fn=%s error=%r elapsed=%.1fs",
                   fn_name, exc[0], elapsed)
        raise exc[0]

    _log.info("AGENT_DONE fn=%s elapsed=%.1fs", fn_name, elapsed)
    return result[0] if result else None


def watch(fn: Callable, *args: Any, timeout: int = TIMEOUT_SECONDS,
          **kwargs: Any) -> Any:
    """Run *fn* with a hard timeout; log all decisions to agent_trace.log."""
    return _run_with_timeout(fn, args, kwargs, timeout)


def guarded(timeout: int = TIMEOUT_SECONDS) -> Callable[[Callable], Callable]:
    """Decorator: wrap any agent callable with Watchdog protection."""
    def decorator(fn: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return watch(fn, *args, timeout=timeout, **kwargs)
        wrapper.__wrapped__ = fn
        return wrapper
    return decorator
