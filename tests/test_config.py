import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from src.config import Settings

_K = {"ANTHROPIC_API_KEY": "x", "PERPLEXITY_API_KEY": "x"}


def test_settings_load_from_env():
    s = Settings(ANTHROPIC_API_KEY="sk-test", PERPLEXITY_API_KEY="p")
    assert s.ANTHROPIC_API_KEY == "sk-test"


def test_llm_model_default(monkeypatch):
    monkeypatch.delenv("LLM_MODEL", raising=False)
    assert Settings(**_K).LLM_MODEL == "anthropic/claude-haiku-4-5-20251001"


def test_max_agent_retries_default():
    assert Settings(**_K).MAX_AGENT_RETRIES == 2


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
    with patch.dict(os.environ, {}, clear=True), pytest.raises(ValidationError):
        Settings()


def test_missing_perplexity_api_key_raises():
    with (
        patch.dict(os.environ, {"ANTHROPIC_API_KEY": "x"}, clear=True),
        pytest.raises(ValidationError),
    ):
        Settings()


def test_perplexity_api_key_loaded():
    s = Settings(ANTHROPIC_API_KEY="x", PERPLEXITY_API_KEY="pplx-test")
    assert s.PERPLEXITY_API_KEY == "pplx-test"


def test_biber_bin_default():
    assert Settings(**_K).BIBER_BIN == "biber"


def test_pandoc_bin_default():
    assert Settings(**_K).PANDOC_BIN == "pandoc"


def test_perplexity_api_url_default():
    url = Settings(**_K).PERPLEXITY_API_URL
    assert "perplexity.ai" in url


def test_perplexity_api_url_override(monkeypatch):
    monkeypatch.setenv("PERPLEXITY_API_URL", "https://custom.example.com/v1")
    assert Settings(**_K).PERPLEXITY_API_URL == "https://custom.example.com/v1"


def test_max_iter_default():
    assert Settings(**_K).MAX_ITER == 80


def test_max_tokens_default():
    assert Settings(**_K).MAX_TOKENS == 4096


def test_max_iter_override(monkeypatch):
    monkeypatch.setenv("MAX_ITER", "10")
    assert Settings(**_K).MAX_ITER == 10


def test_max_tokens_override(monkeypatch):
    monkeypatch.setenv("MAX_TOKENS", "2048")
    assert Settings(**_K).MAX_TOKENS == 2048


def test_env_override_llm_model(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "claude-opus-4-8")
    assert Settings(**_K).LLM_MODEL == "claude-opus-4-8"


def test_env_override_min_pages(monkeypatch):
    monkeypatch.setenv("MIN_PAGES", "20")
    assert Settings(**_K).MIN_PAGES == 20
