"""Tests for V3 architecture: RouterSkill, Watchdog, DebateReviewer."""
import time
from unittest.mock import patch

import pytest


# ── RouterSkill ────────────────────────────────────────────────────────────
class TestWCLedger:
    def test_record_accumulates(self):
        from src.skills.router_skill import WCLedger
        ledger = WCLedger()
        wc = ledger.record(q=10, r=5, a=2)
        assert wc == 17
        wc2 = ledger.record(q=3, r=3, a=0)
        assert wc2 == 23

    def test_savings_vs_eager(self):
        from src.skills.router_skill import WCLedger
        ledger = WCLedger()
        ledger.record(q=10, r=10, a=5)
        ledger.record(q=10, r=10, a=0)
        savings = ledger.savings_vs_eager(eager_load_tokens=20)
        assert savings >= 0

    def test_empty_ledger_savings(self):
        from src.skills.router_skill import WCLedger
        ledger = WCLedger()
        assert ledger.savings_vs_eager(50) == 0

    def test_rounds_tracked(self):
        from src.skills.router_skill import WCLedger
        ledger = WCLedger()
        ledger.record(1, 2, 3)
        ledger.record(4, 5, 6)
        assert len(ledger.rounds) == 2
        assert ledger.rounds[0]["wc"] == 6


class TestRouterSkillFunctions:
    def test_loaded_skills_initially_empty(self):
        import importlib

        import src.skills.router_skill as rs
        importlib.reload(rs)
        assert rs.loaded_skills() == []

    def test_get_ledger_returns_ledger(self):
        from src.skills import router_skill as rs
        assert rs.get_ledger() is not None

    def test_route_unknown_skill_raises(self):
        from src.skills import router_skill as rs
        with pytest.raises(KeyError, match="Unknown skill"):
            rs.route("nonexistent_skill_xyz", "test query")


# ── Watchdog ───────────────────────────────────────────────────────────────
class TestAgentWatchdog:
    def test_watch_completes_fast_fn(self):
        from src.watchdog.agent_watchdog import watch
        result = watch(lambda: 42, timeout=5)
        assert result == 42

    def test_watch_passes_args(self):
        from src.watchdog.agent_watchdog import watch
        result = watch(lambda x, y: x + y, 3, 7, timeout=5)
        assert result == 10

    def test_watch_raises_on_timeout(self):
        from src.watchdog.agent_watchdog import WatchdogTimeoutError, watch
        with pytest.raises(WatchdogTimeoutError):
            watch(time.sleep, 10, timeout=1)

    def test_watch_propagates_exceptions(self):
        from src.watchdog.agent_watchdog import watch
        def bad():
            raise ValueError("oops")
        with pytest.raises(ValueError, match="oops"):
            watch(bad, timeout=5)

    def test_guarded_decorator(self):
        from src.watchdog.agent_watchdog import guarded
        @guarded(timeout=5)
        def fast():
            return "ok"
        assert fast() == "ok"

    def test_watchdog_timeout_error_is_runtime(self):
        from src.watchdog.agent_watchdog import WatchdogTimeoutError
        assert issubclass(WatchdogTimeoutError, RuntimeError)


# ── DebateReviewer (mocked API) ────────────────────────────────────────────
class TestDebateReviewer:
    def _mock_call(self, system, user):
        if "Deep Learning" in system:
            return "Good architecture. Needs ablation study."
        return "Good Hebrew RTL. Citation style correct."

    def test_review_reaches_consensus(self):
        from src.debate_agents import debate_reviewer as dr
        with patch.object(dr, "_call", side_effect=self._mock_call):
            result = dr.review("draft text", max_rounds=3,
                               consensus_threshold=0.01)
        assert result.dl_review != ""
        assert result.nlp_review != ""
        assert result.rounds >= 1

    def test_review_result_dataclass(self):
        from src.debate_agents.debate_reviewer import ReviewResult
        r = ReviewResult("dl", "nlp", "consensus", rounds=2, agreed=True)
        assert r.agreed is True
        assert r.rounds == 2

    def test_cosine_sim_identical(self):
        from src.debate_agents.debate_reviewer import _cosine_sim_approx
        result = _cosine_sim_approx("hello world", "hello world")
        assert result == pytest.approx(1.0, abs=0.01)

    def test_cosine_sim_disjoint(self):
        from src.debate_agents.debate_reviewer import _cosine_sim_approx
        assert _cosine_sim_approx("abc def", "xyz uvw") == pytest.approx(0.0, abs=0.01)
