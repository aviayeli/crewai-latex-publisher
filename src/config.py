"""Centralised configuration loaded from environment / .env via pydantic-settings."""

import contextlib
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
    # 60 RPM matches Anthropic Tier-1 limits; override via .env for higher tiers.
    GATEKEEPER_RPM: int = 60
    # When True, caps max_tokens=10 on every LLM call so the pipeline can be
    # smoke-tested end-to-end without meaningful API spend.
    DRY_RUN: bool = False


# ── Lazy singletons ──────────────────────────────────────────────────────────

_settings_obj: "Settings | None" = None
_gatekeeper_obj: "ApiGatekeeper | None" = None


def get_settings() -> Settings:
    """Return (and lazily construct) the Settings singleton."""
    global _settings_obj
    if _settings_obj is None:
        _settings_obj = Settings(_env_file=".env")
    return _settings_obj


class _Lazy:
    """Defers singleton construction; caches attrs for mock.patch compatibility."""

    def __init__(self, factory: Any) -> None:
        object.__setattr__(self, "_f", factory)

    @property
    def __class__(self) -> type:  # type: ignore[override]
        return type(object.__getattribute__(self, "_f")())

    def __getattr__(self, name: str) -> Any:
        value = getattr(object.__getattribute__(self, "_f")(), name)
        object.__setattr__(self, name, value)  # cache → is_local=True for mock.patch
        return value

    def __setattr__(self, name: str, value: Any) -> None:
        object.__setattr__(self, name, value)  # update local cache
        setattr(object.__getattribute__(self, "_f")(), name, value)

    def __delattr__(self, name: str) -> None:
        for obj in (self, object.__getattribute__(self, "_f")()):
            with contextlib.suppress(AttributeError):
                object.__delattr__(obj, name)


def _get_gatekeeper() -> ApiGatekeeper:
    global _gatekeeper_obj
    if _gatekeeper_obj is None:
        _gatekeeper_obj = ApiGatekeeper(
            calls_per_minute=get_settings().GATEKEEPER_RPM
        )
    return _gatekeeper_obj


settings: Any = _Lazy(get_settings)
gatekeeper: Any = _Lazy(_get_gatekeeper)


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

    max_tok = 10 if settings.DRY_RUN else settings.MAX_TOKENS
    kwargs: dict = {"model": model, "max_tokens": max_tok}
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
