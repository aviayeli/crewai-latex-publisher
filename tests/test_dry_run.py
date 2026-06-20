"""Tests for DRY_RUN configuration flag (TDD — written before implementation)."""
from unittest.mock import MagicMock, patch

_K = {"ANTHROPIC_API_KEY": "x", "PERPLEXITY_API_KEY": "x"}


class TestDryRunSetting:
    def test_default_is_false(self):
        from src.config import Settings
        assert Settings(**_K).DRY_RUN is False

    def test_can_be_enabled_via_env(self, monkeypatch):
        monkeypatch.setenv("DRY_RUN", "true")
        from src.config import Settings
        assert Settings(**_K).DRY_RUN is True

    def test_false_uses_normal_max_tokens(self):
        import src.config as cfg
        mock_llm_cls = MagicMock(return_value="llm")
        with (
            patch.object(cfg.settings, "DRY_RUN", False),
            patch("crewai.LLM", mock_llm_cls),
        ):
            cfg._make_llm("anthropic/test-model")
        kwargs = mock_llm_cls.call_args[1]
        assert kwargs["max_tokens"] == cfg.settings.MAX_TOKENS

    def test_true_caps_max_tokens_to_ten(self):
        import src.config as cfg
        mock_llm_cls = MagicMock(return_value="llm")
        with (
            patch.object(cfg.settings, "DRY_RUN", True),
            patch("crewai.LLM", mock_llm_cls),
        ):
            cfg._make_llm("anthropic/test-model")
        kwargs = mock_llm_cls.call_args[1]
        assert kwargs["max_tokens"] == 10
