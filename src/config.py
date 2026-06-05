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
    # Haiku is ~20x cheaper than Sonnet; override via LLM_MODEL= in .env
    LLM_MODEL: str = "anthropic/claude-haiku-4-5-20251001"
    MAX_AGENT_RETRIES: int = 3
    # Max tool-call iterations per agent turn; prevents runaway loops
    MAX_ITER: int = 15
    # Hard output cap per LLM call; keeps per-call cost bounded
    MAX_TOKENS: int = 4096
    PYTHON_RUNNER_TIMEOUT_S: int = 60
    LUALATEX_BIN: str = "lualatex"
    BIBER_BIN: str = "biber"
    PANDOC_BIN: str = "pandoc"
    OUTPUT_DIR: str = "latex_output"
    ASSETS_DIR: str = "latex_output/assets"
    MIN_PAGES: int = 15
    # Set to True to pause before lualatex_runner executes and prompt operator
    HITL_ENABLED: bool = False
    # Passes anthropic-beta prompt-caching header via LiteLLM additional_params
    PROMPT_CACHING_ENABLED: bool = True


settings = Settings(_env_file=".env")


def build_llm():
    """Return a crewai.LLM bound to the current settings (model + token cap).

    When ``PROMPT_CACHING_ENABLED`` is true, the Anthropic prompt-caching beta
    header is injected via LiteLLM ``additional_params`` so system prompts and
    repeated LaTeX preambles are served from Anthropic's cache tier.
    """
    from crewai import LLM  # local import — avoids crewai dep at module load time

    kwargs: dict = {"model": settings.LLM_MODEL, "max_tokens": settings.MAX_TOKENS}
    if settings.PROMPT_CACHING_ENABLED:
        kwargs["additional_params"] = {
            "extra_headers": {"anthropic-beta": "prompt-caching-2024-07-31"}
        }
    return LLM(**kwargs)
