from unittest.mock import MagicMock, patch

from src.config import Settings, build_llm, build_llm_fast, build_llm_smart, settings

_K = {"ANTHROPIC_API_KEY": "x", "PERPLEXITY_API_KEY": "x"}


# ── PROMPT_CACHING_ENABLED ────────────────────────────────────────────────────


def test_prompt_caching_enabled_default_is_true():
    assert Settings(**_K).PROMPT_CACHING_ENABLED is True


def test_hitl_enabled_default_is_true():
    assert Settings(**_K).HITL_ENABLED is True


def test_build_llm_fast_uses_fast_model(monkeypatch):
    monkeypatch.setattr(settings, "PROMPT_CACHING_ENABLED", False)
    with patch("crewai.LLM") as MockLLM:
        MockLLM.return_value = MagicMock()
        build_llm_fast()
    assert MockLLM.call_args.kwargs["model"] == settings.LLM_MODEL_FAST


def test_build_llm_smart_uses_smart_model(monkeypatch):
    monkeypatch.setattr(settings, "PROMPT_CACHING_ENABLED", False)
    with patch("crewai.LLM") as MockLLM:
        MockLLM.return_value = MagicMock()
        build_llm_smart()
    assert MockLLM.call_args.kwargs["model"] == settings.LLM_MODEL_SMART


def test_prompt_caching_can_be_disabled_via_env(monkeypatch):
    monkeypatch.setenv("PROMPT_CACHING_ENABLED", "false")
    assert Settings(**_K).PROMPT_CACHING_ENABLED is False


def test_build_llm_passes_cache_header_when_enabled(monkeypatch):
    monkeypatch.setattr(settings, "PROMPT_CACHING_ENABLED", True)
    with patch("crewai.LLM") as MockLLM:
        MockLLM.return_value = MagicMock()
        build_llm()
    extra = MockLLM.call_args.kwargs.get("additional_params", {})
    header = extra.get("extra_headers", {}).get("anthropic-beta", "")
    assert "prompt-caching" in header


def test_build_llm_omits_cache_params_when_disabled(monkeypatch):
    monkeypatch.setattr(settings, "PROMPT_CACHING_ENABLED", False)
    with patch("crewai.LLM") as MockLLM:
        MockLLM.return_value = MagicMock()
        build_llm()
    assert "additional_params" not in MockLLM.call_args.kwargs


# ── __version__ ───────────────────────────────────────────────────────────────


def test_src_package_exports_version():
    from src import __version__

    assert isinstance(__version__, str) and __version__


def test_src_version_matches_pyproject():
    from src import __version__

    assert __version__ == "0.1.0"
