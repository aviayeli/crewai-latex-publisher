"""Centralised configuration loaded from environment / .env via pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict

_PERPLEXITY_DEFAULT_URL = "https://api.perplexity.ai/chat/completions"


class Settings(BaseSettings):
    """Application settings.

    All values are read from environment variables or a .env file.
    Required fields (ANTHROPIC_API_KEY, PERPLEXITY_API_KEY) have no defaults
    and will raise ValidationError if absent.
    """

    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding="utf-8",
    )

    ANTHROPIC_API_KEY: str
    PERPLEXITY_API_KEY: str
    PERPLEXITY_API_URL: str = _PERPLEXITY_DEFAULT_URL
    # Default model (backward-compat); individual tiers override this.
    LLM_MODEL: str = "anthropic/claude-haiku-4-5-20251001"
    # Tier-1 (fast/cheap): structural agents — outline, compiler, manager.
    LLM_MODEL_FAST: str = "anthropic/claude-haiku-4-5-20251001"
    # Tier-2 (reasoning): content writer and BiDi validator.
    LLM_MODEL_SMART: str = "anthropic/claude-sonnet-4-6"
    MAX_AGENT_RETRIES: int = 3
    # Max tool-call iterations per agent turn; prevents runaway loops
    MAX_ITER: int = 80
    # Hard output cap per LLM call; keeps per-call cost bounded
    MAX_TOKENS: int = 4096
    PYTHON_RUNNER_TIMEOUT_S: int = 60
    LUALATEX_BIN: str = "lualatex"
    BIBER_BIN: str = "biber"
    PANDOC_BIN: str = "pandoc"
    OUTPUT_DIR: str = "latex_output"
    ASSETS_DIR: str = "latex_output/assets"
    MIN_PAGES: int = 15
    # Pause before lualatex_runner executes and prompt operator for approval.
    HITL_ENABLED: bool = True
    # Passes anthropic-beta prompt-caching header via LiteLLM additional_params
    PROMPT_CACHING_ENABLED: bool = True


settings = Settings(_env_file=".env")


def _make_llm(model: str):
    """Shared LLM factory; injects prompt-caching header when enabled."""
    from crewai import LLM  # local import — avoids crewai dep at module load time

    kwargs: dict = {"model": model, "max_tokens": settings.MAX_TOKENS}
    if settings.PROMPT_CACHING_ENABLED:
        kwargs["additional_params"] = {
            "extra_headers": {"anthropic-beta": "prompt-caching-2024-07-31"}
        }
    return LLM(**kwargs)


def build_llm():
    """Default LLM — backward-compatible entry point."""
    return _make_llm(settings.LLM_MODEL)


def build_llm_fast():
    """Tier-1 LLM (Haiku) for structural agents: outline, compiler, manager."""
    return _make_llm(settings.LLM_MODEL_FAST)


def build_llm_smart():
    """Tier-2 LLM (Sonnet) for reasoning agents: content writer, BiDi validator."""
    return _make_llm(settings.LLM_MODEL_SMART)
