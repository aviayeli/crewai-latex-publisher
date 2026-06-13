"""Tests for the CLI entry point — topic menu selection and SDK delegation."""

import sys
from unittest.mock import patch

import pytest

from src.cli import main
from src.topics import TOPICS

_TOPIC_15 = TOPICS[0]  # Sine Wave / Deep Learning cluster
_TOPIC_16 = TOPICS[1]  # Supply Chain / Agent Architecture cluster


# ── run command ───────────────────────────────────────────────────────────────


def test_cli_run_calls_select_topic(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["latex-publisher", "run"])
    with (
        patch("src.cli.select_topic", return_value=_TOPIC_15) as mock_sel,
        patch("src.cli.LatexPublisherSDK") as mock_sdk,
    ):
        mock_sdk.return_value.run.return_value = "done"
        main()
    mock_sel.assert_called_once()


def test_cli_run_passes_title_and_focus_to_sdk(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["latex-publisher", "run"])
    with (
        patch("src.cli.select_topic", return_value=_TOPIC_15),
        patch("src.cli.LatexPublisherSDK") as mock_sdk,
    ):
        mock_sdk.return_value.run.return_value = "done"
        main()
    mock_sdk.return_value.run.assert_called_once_with(
        topic=_TOPIC_15.title,
        research_focus=_TOPIC_15.research_focus,
    )


def test_cli_run_no_args_also_calls_select_topic(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["latex-publisher"])
    with (
        patch("src.cli.select_topic", return_value=_TOPIC_16) as mock_sel,
        patch("src.cli.LatexPublisherSDK") as mock_sdk,
    ):
        mock_sdk.return_value.run.return_value = "done"
        main()
    mock_sel.assert_called_once()
    mock_sdk.return_value.run.assert_called_once_with(
        topic=_TOPIC_16.title,
        research_focus=_TOPIC_16.research_focus,
    )


# ── non-run commands do not trigger the menu ──────────────────────────────────


def test_cli_version_does_not_call_select_topic(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["latex-publisher", "--version"])
    with (
        patch("src.cli.LatexPublisherSDK") as mock_sdk,
        patch("src.cli.select_topic") as mock_sel,
    ):
        mock_sdk.return_value.version = "0.1.0"
        main()
    mock_sel.assert_not_called()


def test_cli_help_does_not_call_select_topic(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["latex-publisher", "--help"])
    with (
        patch("src.cli.LatexPublisherSDK"),
        patch("src.cli.select_topic") as mock_sel,
    ):
        main()
    mock_sel.assert_not_called()


def test_cli_unknown_command_exits_1(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["latex-publisher", "badcmd"])
    with (
        patch("src.cli.LatexPublisherSDK"),
        patch("src.cli.select_topic"),
        pytest.raises(SystemExit) as exc,
    ):
        main()
    assert exc.value.code == 1
