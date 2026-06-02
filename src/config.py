from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding="utf-8",
    )

    ANTHROPIC_API_KEY: str
    PERPLEXITY_API_KEY: str
    LLM_MODEL: str = "claude-sonnet-4-6"
    MAX_AGENT_RETRIES: int = 3
    PYTHON_RUNNER_TIMEOUT_S: int = 60
    LUALATEX_BIN: str = "lualatex"
    BIBER_BIN: str = "biber"
    PANDOC_BIN: str = "pandoc"
    OUTPUT_DIR: str = "latex_output"
    ASSETS_DIR: str = "latex_output/assets"
    MIN_PAGES: int = 15


settings = Settings(_env_file=".env")
