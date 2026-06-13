"""Tests for ApiGatekeeper and FinOpsMixin (TDD — written before implementation)."""
import pytest


class TestFinOpsMixin:
    """FinOpsMixin provides per-instance token and call tracking."""

    def _make(self):
        from src.utils.mixins import FinOpsMixin

        class _C(FinOpsMixin):
            def __init__(self):
                self._init_finops()

        return _C()

    def test_initial_total_tokens_is_zero(self):
        assert self._make().total_tokens == 0

    def test_initial_call_count_is_zero(self):
        assert self._make().call_count == 0

    def test_record_tokens_accumulates(self):
        c = self._make()
        c.record_tokens(100, 50)
        assert c.total_tokens == 150

    def test_call_count_increments_on_each_record(self):
        c = self._make()
        c.record_tokens(10, 5)
        c.record_tokens(20, 10)
        assert c.call_count == 2

    def test_total_tokens_sums_prompt_and_completion(self):
        c = self._make()
        c.record_tokens(300, 200)
        assert c.total_tokens == 500

    def test_reset_clears_all_counters(self):
        c = self._make()
        c.record_tokens(100, 50)
        c.reset_finops()
        assert c.total_tokens == 0
        assert c.call_count == 0


class TestApiGatekeeper:
    """ApiGatekeeper wraps factory calls with rate limiting and FinOps tracking."""

    def test_inherits_finops_mixin(self):
        from src.utils.api_gatekeeper import ApiGatekeeper
        from src.utils.mixins import FinOpsMixin

        assert issubclass(ApiGatekeeper, FinOpsMixin)

    def test_guard_invokes_and_returns_factory_result(self):
        from src.utils.api_gatekeeper import ApiGatekeeper

        sentinel = object()
        assert ApiGatekeeper().guard(lambda: sentinel) is sentinel

    def test_guard_increments_call_count(self):
        from src.utils.api_gatekeeper import ApiGatekeeper

        gk = ApiGatekeeper()
        gk.guard(lambda: None)
        gk.guard(lambda: None)
        assert gk.call_count == 2

    def test_rate_limit_raises_on_exceeded(self):
        from src.utils.api_gatekeeper import ApiGatekeeper, RateLimitExceededError

        gk = ApiGatekeeper(calls_per_minute=2)
        gk.guard(lambda: None)
        gk.guard(lambda: None)
        with pytest.raises(RateLimitExceededError):
            gk.guard(lambda: None)

    def test_rate_limit_allows_exact_limit(self):
        from src.utils.api_gatekeeper import ApiGatekeeper

        gk = ApiGatekeeper(calls_per_minute=3)
        for _ in range(3):
            gk.guard(lambda: None)  # must not raise

    def test_rate_limit_error_is_runtime_error(self):
        from src.utils.api_gatekeeper import RateLimitExceededError

        assert issubclass(RateLimitExceededError, RuntimeError)


class TestGatekeeperInConfig:
    """config module exposes a gatekeeper singleton that routes all build_llm calls."""

    def test_gatekeeper_is_api_gatekeeper_instance(self):
        from src.config import gatekeeper
        from src.utils.api_gatekeeper import ApiGatekeeper

        assert isinstance(gatekeeper, ApiGatekeeper)

    def test_build_llm_routed_through_gatekeeper(self):
        from unittest.mock import MagicMock, patch

        import src.config as cfg

        mock_guard = MagicMock(return_value=MagicMock())
        with patch.object(cfg.gatekeeper, "guard", mock_guard):
            cfg.build_llm()
        mock_guard.assert_called_once()

    def test_build_llm_fast_routed_through_gatekeeper(self):
        from unittest.mock import MagicMock, patch

        import src.config as cfg

        mock_guard = MagicMock(return_value=MagicMock())
        with patch.object(cfg.gatekeeper, "guard", mock_guard):
            cfg.build_llm_fast()
        mock_guard.assert_called_once()

    def test_build_llm_smart_routed_through_gatekeeper(self):
        from unittest.mock import MagicMock, patch

        import src.config as cfg

        mock_guard = MagicMock(return_value=MagicMock())
        with patch.object(cfg.gatekeeper, "guard", mock_guard):
            cfg.build_llm_smart()
        mock_guard.assert_called_once()


class TestSDKInheritsFinOpsMixin:
    """LatexPublisherSDK must inherit FinOpsMixin (V3 mixin OOP requirement)."""

    def test_sdk_is_finops_mixin_subclass(self):
        from src.sdk.latex_publisher_sdk import LatexPublisherSDK
        from src.utils.mixins import FinOpsMixin

        assert issubclass(LatexPublisherSDK, FinOpsMixin)

    def test_sdk_exposes_finops_interface(self):
        from src.sdk.latex_publisher_sdk import LatexPublisherSDK

        sdk = LatexPublisherSDK()
        assert hasattr(sdk, "record_tokens")
        assert sdk.total_tokens == 0
