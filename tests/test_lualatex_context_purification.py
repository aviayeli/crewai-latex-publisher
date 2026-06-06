"""Tests for _parse_log context purification: warning capture and non-blocking."""

from unittest.mock import MagicMock, patch

from src.config import settings
from src.tools.lualatex_runner import lualatex_runner_tool


def test_log_parser_captures_latex_warning_lines(tmp_path):
    log = tmp_path / "main.log"
    log.write_text("LaTeX Warning: Reference 'fig:foo' on page 1 undefined.\n")
    lines = lualatex_runner_tool._parse_log(log)
    assert len(lines) > 0


def test_log_parser_captures_package_warning_lines(tmp_path):
    log = tmp_path / "main.log"
    log.write_text(
        "Package hyperref Warning: Token not allowed in a PDF string.\n"
    )
    lines = lualatex_runner_tool._parse_log(log)
    assert len(lines) > 0


def test_log_parser_warnings_do_not_abort_successful_run(tmp_path, monkeypatch):
    """Warnings alone must NOT block a successful compilation."""
    monkeypatch.setattr(settings, "OUTPUT_DIR", str(tmp_path))
    monkeypatch.setattr(settings, "HITL_ENABLED", False)
    (tmp_path / "main.log").write_text(
        "LaTeX Warning: Label(s) may have changed. Rerun.\n"
    )
    with patch("src.tools.lualatex_runner.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        result = lualatex_runner_tool._run(
            tex_file="main.tex", passes=1, run_biber=False
        )
    assert result.get("success") is True
