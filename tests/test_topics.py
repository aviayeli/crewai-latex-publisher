"""Tests for the topic registry, ASCII menu, and interactive selection."""

from unittest.mock import patch

import pytest

from src.topics import TOPICS, Topic, display_menu, select_topic

# ── TOPICS registry ───────────────────────────────────────────────────────────


def test_topics_has_exactly_four_entries():
    assert len(TOPICS) == 4


def test_display_ids_are_15_through_18():
    assert [t.display_id for t in TOPICS] == [15, 16, 17, 18]


def test_topics_1_and_3_focus_on_deep_learning():
    assert "Deep Learning" in TOPICS[0].research_focus
    assert "Deep Learning" in TOPICS[2].research_focus


def test_topics_2_and_4_focus_on_agent_architecture():
    assert "Agent" in TOPICS[1].research_focus
    assert "Agent" in TOPICS[3].research_focus


def test_topics_2_and_4_mention_mcp():
    assert "MCP" in TOPICS[1].research_focus
    assert "MCP" in TOPICS[3].research_focus


def test_each_topic_has_non_empty_title():
    assert all(t.title for t in TOPICS)


def test_topic_is_frozen_dataclass():
    with pytest.raises((AttributeError, TypeError)):
        TOPICS[0].title = "mutated"  # type: ignore[misc]


def test_topic_dataclass_equality():
    t = Topic(display_id=15, title="x", research_focus="y")
    assert t == Topic(display_id=15, title="x", research_focus="y")


# ── display_menu ─────────────────────────────────────────────────────────────


def test_display_menu_prints_all_display_ids(capsys):
    display_menu()
    out = capsys.readouterr().out
    for i in (15, 16, 17, 18):
        assert str(i) in out


def test_display_menu_prints_all_positional_numbers(capsys):
    display_menu()
    out = capsys.readouterr().out
    for i in range(1, 5):
        assert f"({i})" in out


# ── select_topic ──────────────────────────────────────────────────────────────


def test_select_topic_choice_1_returns_topic_15():
    with patch("builtins.input", return_value="1"):
        selected = select_topic()
    assert selected.display_id == 15


def test_select_topic_choice_2_returns_topic_16():
    with patch("builtins.input", return_value="2"):
        selected = select_topic()
    assert selected.display_id == 16


def test_select_topic_choice_3_returns_topic_17():
    with patch("builtins.input", return_value="3"):
        selected = select_topic()
    assert selected.display_id == 17


def test_select_topic_choice_4_returns_topic_18():
    with patch("builtins.input", return_value="4"):
        selected = select_topic()
    assert selected.display_id == 18


def test_select_topic_retries_on_invalid_then_accepts_valid():
    with patch("builtins.input", side_effect=["0", "bad", "99", "3"]):
        selected = select_topic()
    assert selected.display_id == 17


def test_select_topic_returns_topic_instance():
    with patch("builtins.input", return_value="2"):
        selected = select_topic()
    assert isinstance(selected, Topic)
