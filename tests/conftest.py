from pathlib import Path
from unittest import mock

import pytest

from src.config import Settings


@pytest.fixture(scope="function")
def tmp_output_dir(tmp_path: Path):
    (tmp_path / "assets").mkdir()
    (tmp_path / "chapters").mkdir()
    (tmp_path / "figures").mkdir()
    with (
        mock.patch("src.config.settings.OUTPUT_DIR", str(tmp_path)),
        mock.patch("src.config.settings.ASSETS_DIR", str(tmp_path / "assets")),
    ):
        yield tmp_path


@pytest.fixture
def mock_settings() -> Settings:
    return Settings(
        ANTHROPIC_API_KEY="test-key-placeholder",
        PERPLEXITY_API_KEY="test-pplx-placeholder",
        LLM_MODEL="claude-haiku-4-5-20251001",
        MAX_AGENT_RETRIES=1,
        PYTHON_RUNNER_TIMEOUT_S=10,
    )
