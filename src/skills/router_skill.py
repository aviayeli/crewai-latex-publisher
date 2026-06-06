"""Router-Skill: lazy-load LaTeX skills only when needed, tracking token savings."""
from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import Any

from src.config import settings


@dataclass
class WCLedger:
    """Token-economics counters: WC_n = WC_{n-1} + Q_n + R_n + A_n."""
    total: int = 0
    rounds: list[dict] = field(default_factory=list)

    def record(self, q: int, r: int, a: int) -> int:
        self.total += q + r + a
        self.rounds.append({"q": q, "r": r, "a": a, "wc": self.total})
        return self.total

    def savings_vs_eager(self, eager_load_tokens: int) -> int:
        return max(0, eager_load_tokens * len(self.rounds) - self.total)


_SKILL_REGISTRY: dict[str, str] = {
    "latex_writer":     "src.tools.latex_writer",
    "lualatex_runner":  "src.tools.lualatex_runner",
    "markdown_conv":    "src.tools.markdown_converter",
    "python_runner":    "src.tools.python_runner",
    "perplexity":       "src.tools.perplexity_search",
}

_loaded: dict[str, Any] = {}
_ledger = WCLedger()


def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def route(skill_name: str, query: str, context: str = "") -> tuple[Any, WCLedger]:
    """Return the requested skill module, loading lazily, and record token usage."""
    q_tokens = _estimate_tokens(query + context)
    a_tokens = 0

    if skill_name not in _loaded:
        if skill_name not in _SKILL_REGISTRY:
            raise KeyError(f"Unknown skill: {skill_name!r}. "
                           f"Available: {list(_SKILL_REGISTRY)}")
        mod_path = _SKILL_REGISTRY[skill_name]
        _loaded[skill_name] = importlib.import_module(mod_path)
        load_cost = _estimate_tokens(mod_path) * settings.MAX_ITER
        a_tokens = load_cost

    skill = _loaded[skill_name]
    r_tokens = _estimate_tokens(repr(skill))
    _ledger.record(q=q_tokens, r=r_tokens, a=a_tokens)
    return skill, _ledger


def get_ledger() -> WCLedger:
    return _ledger


def loaded_skills() -> list[str]:
    return list(_loaded.keys())
