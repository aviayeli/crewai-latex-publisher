"""Tests for the CLI entry point topic-prompt behaviour."""

import sys
from unittest.mock import patch

import pytest

from src.cli import main


def test_cli_run_prompts_user_for_topic(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["latex-publisher", "run"])
    with (
        patch("src.cli.LatexPublisherSDK") as MockSDK,
        patch("builtins.input", return_value="Quantum Computing") as mock_input,
    ):
        MockSDK.return_value.run.return_value = "done"
        main()
    mock_input.assert_called_once()


def test_cli_run_passes_stripped_topic_to_sdk(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["latex-publisher", "run"])
    with (
        patch("src.cli.LatexPublisherSDK") as MockSDK,
        patch("builtins.input", return_value="  Graph Neural Networks  "),
    ):
        MockSDK.return_value.run.return_value = "done"
        main()
    MockSDK.return_value.run.assert_called_once_with(topic="Graph Neural Networks")


def test_cli_run_no_args_also_prompts(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["latex-publisher"])
    with (
        patch("src.cli.LatexPublisherSDK") as MockSDK,
        patch("builtins.input", return_value="LLM Safety") as mock_input,
    ):
        MockSDK.return_value.run.return_value = "done"
        main()
    mock_input.assert_called_once()
    MockSDK.return_value.run.assert_called_once_with(topic="LLM Safety")


def test_cli_version_does_not_prompt(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["latex-publisher", "--version"])
    with (
        patch("src.cli.LatexPublisherSDK") as MockSDK,
        patch("builtins.input") as mock_input,
    ):
        MockSDK.return_value.version = "0.1.0"
        main()
    mock_input.assert_not_called()


def test_cli_help_does_not_prompt(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["latex-publisher", "--help"])
    with (
        patch("src.cli.LatexPublisherSDK"),
        patch("builtins.input") as mock_input,
    ):
        main()
    mock_input.assert_not_called()


def test_cli_unknown_command_exits_1(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["latex-publisher", "badcmd"])
    with (
        patch("src.cli.LatexPublisherSDK"),
        patch("builtins.input"),
        pytest.raises(SystemExit) as exc,
    ):
        main()
    assert exc.value.code == 1
