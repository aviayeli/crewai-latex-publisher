"""Tests for the dedicated AbstractTask factory."""
from unittest.mock import patch

import pytest

from src.crew import PublisherCrew

pytestmark = pytest.mark.usefixtures("mock_llm_creation")


def test_abstract_task_exists_in_crew():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert hasattr(crew, "abstract_task")


def test_abstract_task_description_mentions_abstract():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    desc = crew.abstract_task.description
    assert "abstract" in desc.lower() or "תקציר" in desc


def test_abstract_task_description_mentions_prepend():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert "prepend" in crew.abstract_task.description.lower()


def test_abstract_task_agent_is_content_agent():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert crew.abstract_task.agent is crew.content_agent


def test_abstract_task_context_contains_bidi_task():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert crew.bidi_task in crew.abstract_task.context
