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


settings = Settings(_env_file=".env")


def build_llm():
    """Return a crewai.LLM bound to the current settings (model + token cap)."""
    from crewai import LLM  # local import — avoids crewai dep at module load time

    return LLM(model=settings.LLM_MODEL, max_tokens=settings.MAX_TOKENS)
