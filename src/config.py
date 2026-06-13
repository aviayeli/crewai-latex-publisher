"""Centralised configuration loaded from environment / .env via pydantic-settings."""

from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils.api_gatekeeper import ApiGatekeeper

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
    MAX_AGENT_RETRIES: int = 2
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
    TEMPLATES_DIR: str = "templates"
    MIN_PAGES: int = 15
    # Hard timeout (seconds) for the full pipeline run via the watchdog.
    WATCHDOG_TIMEOUT: int = 3600
    # Pause before lualatex_runner executes and prompt operator for approval.
    HITL_ENABLED: bool = True
    # Passes anthropic-beta prompt-caching header via LiteLLM additional_params
    PROMPT_CACHING_ENABLED: bool = True
    # Maximum LLM factory calls per 60-second window enforced by ApiGatekeeper.
    # High default so local/CI runs are not throttled; lower via .env in production.
    GATEKEEPER_RPM: int = 10000


settings = Settings(_env_file=".env")
gatekeeper = ApiGatekeeper(calls_per_minute=settings.GATEKEEPER_RPM)


def _make_llm(model: str) -> Any:
    """Shared LLM factory; injects prompt-caching header when enabled.

    Cache boundary: the Anthropic system message (static cacheable prefix)
    contains agent role + goal + backstory (SKILL.md content) + TTC tool
    descriptions.  Dynamic content — tool call results, search responses,
    and compilation logs — lands exclusively in conversation turns and is
    therefore outside the cached prefix.  This boundary is preserved
    automatically by CrewAI's hierarchical process; no further action is
    required in individual agents.
    """
    from crewai import LLM  # local import — avoids crewai dep at module load time

    kwargs: dict = {"model": model, "max_tokens": settings.MAX_TOKENS}
    if settings.PROMPT_CACHING_ENABLED:
        kwargs["additional_params"] = {
            "extra_headers": {"anthropic-beta": "prompt-caching-2024-07-31"}
        }
    return LLM(**kwargs)


def build_llm() -> Any:
    """Default LLM — backward-compatible entry point."""
    return gatekeeper.guard(lambda: _make_llm(settings.LLM_MODEL))


def build_llm_fast() -> Any:
    """Tier-1 LLM (Haiku) for structural agents: outline, compiler, manager."""
    return gatekeeper.guard(lambda: _make_llm(settings.LLM_MODEL_FAST))


def build_llm_smart() -> Any:
    """Tier-2 LLM (Sonnet) for reasoning agents: content writer, BiDi validator."""
    return gatekeeper.guard(lambda: _make_llm(settings.LLM_MODEL_SMART))
