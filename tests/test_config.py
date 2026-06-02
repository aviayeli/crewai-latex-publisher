import os  # noqa: F401
from unittest.mock import patch

import pytest
from pydantic import ValidationError
from src.config import Settings

_K = {"ANTHROPIC_API_KEY": "x", "PERPLEXITY_API_KEY": "x"}


def test_settings_load_from_env():
    s = Settings(ANTHROPIC_API_KEY="sk-test", PERPLEXITY_API_KEY="p")
    assert s.ANTHROPIC_API_KEY == "sk-test"


def test_llm_model_default():
    assert Settings(**_K).LLM_MODEL == "claude-sonnet-4-6"


def test_max_agent_retries_default():
    assert Settings(**_K).MAX_AGENT_RETRIES == 3


def test_python_runner_timeout_default():
    assert Settings(**_K).PYTHON_RUNNER_TIMEOUT_S == 60


def test_lualatex_bin_default():
    assert Settings(**_K).LUALATEX_BIN == "lualatex"


def test_output_dir_default():
    assert Settings(**_K).OUTPUT_DIR == "latex_output"


def test_assets_dir_default():
    assert Settings(**_K).ASSETS_DIR == "latex_output/assets"


def test_min_pages_default():
    assert Settings(**_K).MIN_PAGES == 15


def test_missing_api_key_raises():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValidationError):
            Settings()


def test_missing_perplexity_api_key_raises():
    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "x"}, clear=True):
        with pytest.raises(ValidationError):
            Settings()


def test_perplexity_api_key_loaded():
    s = Settings(ANTHROPIC_API_KEY="x", PERPLEXITY_API_KEY="pplx-test")
    assert s.PERPLEXITY_API_KEY == "pplx-test"


def test_biber_bin_default():
    assert Settings(**_K).BIBER_BIN == "biber"


def test_pandoc_bin_default():
    assert Settings(**_K).PANDOC_BIN == "pandoc"


def test_env_override_llm_model(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "claude-opus-4-8")
    assert Settings(**_K).LLM_MODEL == "claude-opus-4-8"


def test_env_override_min_pages(monkeypatch):
    monkeypatch.setenv("MIN_PAGES", "20")
    assert Settings(**_K).MIN_PAGES == 20
