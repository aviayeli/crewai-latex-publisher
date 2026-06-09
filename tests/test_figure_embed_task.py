"""Tests for the dedicated FigureEmbedTask factory."""
from unittest.mock import patch

import pytest

pytestmark = pytest.mark.usefixtures("mock_llm_creation")


def test_figure_embed_task_exists_in_crew():
    from src.crew import PublisherCrew

    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert hasattr(crew, "figure_embed_task")


def test_figure_embed_task_mentions_ch2():
    from src.crew import PublisherCrew

    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert "ch2" in crew.figure_embed_task.description


def test_figure_embed_task_mentions_ch3():
    from src.crew import PublisherCrew

    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert "ch3" in crew.figure_embed_task.description


def test_figure_embed_task_mentions_includegraphics():
    from src.crew import PublisherCrew

    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert "includegraphics" in crew.figure_embed_task.description.lower()


def test_figure_embed_task_agent_is_figure_agent():
    from src.crew import PublisherCrew

    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert crew.figure_embed_task.agent is crew.figure_agent


def test_figure_embed_task_context_contains_figure_task():
    from src.crew import PublisherCrew

    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert crew.figure_task in crew.figure_embed_task.context
