from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest

from src.config import Settings, settings
from tests.qa_article_data import ARTICLES, ArticleData, load_article


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


@pytest.fixture
def mock_llm_creation():
    mock = MagicMock()
    mock.model = settings.LLM_MODEL
    # Bypass the rate-limit check so that test suites with many PublisherCrew()
    # instantiations don't exhaust the realistic 60-RPM production limit.
    with (
        patch("crewai.agent.core.create_llm", return_value=mock),
        patch("src.config.gatekeeper.guard", side_effect=lambda fn: fn()),
    ):
        yield


@pytest.fixture(params=list(ARTICLES.keys()))
def article(request) -> ArticleData:
    """Parametrised fixture yielding one ArticleData per mass-produced article."""
    name = request.param
    return load_article(name, ARTICLES[name])
