#!/usr/bin/env python3
"""Non-interactive smoke test: validates all pipeline components without real API calls.

Run with DRY_RUN=true in .env (or environment) before spending any API budget.
Every check is deterministic — no network calls are made.
"""
from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import dotenv

dotenv.load_dotenv()

from src.config import _make_llm, settings  # noqa: E402
from src.utils.llm_router import LLMRouter, TaskComplexity  # noqa: E402
from src.utils.mixins import MemoryManagerMixin  # noqa: E402

_PASS = "OK"
_FAIL = "FAIL"


def _check(label: str, ok: bool) -> None:
    status = _PASS if ok else _FAIL
    print(f"  [{status}]  {label}")
    if not ok:
        print("\n[DRY-RUN FAILED] Fix the above check and re-run.\n")
        sys.exit(1)


class _Compactor(MemoryManagerMixin):
    pass


def main() -> None:
    print("\n[DRY-RUN] crewai-latex-publisher — Pipeline Smoke Test")
    print("=" * 55)

    # ── 1. DRY_RUN is active ─────────────────────────────────────
    _check(
        f"DRY_RUN=True in settings (got {settings.DRY_RUN})",
        settings.DRY_RUN is True,
    )

    # ── 2. LLMRouter: COMPLEX → fast in DRY_RUN ──────────────────
    router = LLMRouter()
    with patch("src.utils.llm_router.build_llm_fast", return_value="fast") as m:
        result = router.route(TaskComplexity.COMPLEX)
    _check(
        f"LLMRouter.route(COMPLEX) → build_llm_fast() in DRY_RUN (got {result!r})",
        result == "fast" and m.call_count == 1,
    )

    # ── 3. LLMRouter: SIMPLE → fast in DRY_RUN (no local stub) ───
    router2 = LLMRouter()
    with patch("src.utils.llm_router.build_llm_fast", return_value="fast") as m2:
        result2 = router2.route(TaskComplexity.SIMPLE)
    _check(
        f"LLMRouter.route(SIMPLE) → build_llm_fast() in DRY_RUN (got {result2!r})",
        result2 == "fast" and m2.call_count == 1,
    )

    # ── 4. classify() heuristic ───────────────────────────────────
    r = LLMRouter()
    _check(
        "classify('fix LaTeX syntax') → SIMPLE",
        r.classify("fix LaTeX syntax") == TaskComplexity.SIMPLE,
    )
    _check(
        "classify('structure paper arguments') → COMPLEX",
        r.classify("structure paper arguments") == TaskComplexity.COMPLEX,
    )

    # ── 5. _make_llm caps max_tokens=10 ──────────────────────────
    mock_cls = MagicMock(return_value=MagicMock())
    with patch("crewai.LLM", mock_cls):
        _make_llm("anthropic/claude-haiku-4-5-20251001")
    got_tok = mock_cls.call_args[1]["max_tokens"]
    _check(f"_make_llm() max_tokens={got_tok} (expected 10)", got_tok == 10)

    # ── 6. MemoryManagerMixin compact ────────────────────────────
    c = _Compactor()
    sections = [
        "Chapter 1: Introduction to Transformer architectures",
        "Chapter 2: LSTM and gated recurrent units",
        "Chapter 3: Self-attention and positional encoding",
    ]
    summary = c.compact(sections)
    _check(
        f"compact({len(sections)} sections) → {len(summary)}-char summary with count",
        len(summary) > 0 and "3" in summary,
    )

    # ── 7. active_context shrinks overflow ───────────────────────
    active = c.active_context(sections + ["Chapter 4: Current chapter"], window=1)
    _check(
        f"active_context(4 sections, window=1) → {len(active)} elements (1 summary + 1)",
        len(active) == 2 and active[-1] == "Chapter 4: Current chapter",
    )

    # ── 8. FinOps call tracking ───────────────────────────────────
    router3 = LLMRouter()
    with patch("src.utils.llm_router.build_llm_fast", return_value="f"):
        router3.route(TaskComplexity.COMPLEX)
        router3.route(TaskComplexity.SIMPLE)
    _check(
        f"LLMRouter FinOps.call_count={router3.call_count} (expected 2)",
        router3.call_count == 2,
    )

    # ── 9. Full SDK import chain ──────────────────────────────────
    from src.sdk.latex_publisher_sdk import LatexPublisherSDK  # noqa: PLC0415

    sdk = LatexPublisherSDK()
    _check(
        f"LatexPublisherSDK instantiated (finops={sdk.total_tokens} tokens)",
        sdk.total_tokens == 0,
    )

    print("=" * 55)
    print("[DRY-RUN COMPLETE] 9/9 checks passed.")
    print("  max_tokens=10 enforced  — zero API budget spent")
    print("  LLMRouter bypasses LocalLLMStub in DRY_RUN mode")
    print("  MemoryManagerMixin Compact pattern operational")
    print("  Full SDK import chain verified\n")


if __name__ == "__main__":
    main()
