import shutil
import subprocess
from unittest.mock import patch

import pytest

from src.config import settings
from src.tools.lualatex_runner import CompilationError, lualatex_runner_tool

# ── SkillOpt _suggest_fix ────────────────────────────────────────────────────


def test_suggest_fix_undefined_control_sequence_mentions_package():
    errors = ["! Undefined control sequence."]
    result = lualatex_runner_tool._suggest_fix(errors)
    assert "SkillOpt" in result
    assert "REPLACE" in result or "package" in result.lower()


def test_suggest_fix_missing_dollar_mentions_math():
    errors = ["! Missing $ inserted."]
    result = lualatex_runner_tool._suggest_fix(errors)
    assert "SkillOpt" in result
    assert "ADD" in result or "math" in result.lower()


def test_suggest_fix_file_not_found_mentions_path():
    errors = ["! File 'figure.png' not found."]
    result = lualatex_runner_tool._suggest_fix(errors)
    assert "SkillOpt" in result
    assert "REPLACE" in result or "path" in result.lower()


def test_suggest_fix_begin_document_in_chapter_file():
    errors = ["! Undefined control sequence \\begin{document} in chapter."]
    result = lualatex_runner_tool._suggest_fix(errors)
    assert "SkillOpt" in result


def test_suggest_fix_empty_errors_returns_generic_hint():
    result = lualatex_runner_tool._suggest_fix([])
    assert "SkillOpt" in result


def test_suggest_fix_returns_non_empty_string_for_any_error():
    result = lualatex_runner_tool._suggest_fix(["! Some unknown LaTeX error."])
    assert isinstance(result, str) and result


def test_compilation_error_message_includes_skillopt_hint(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "OUTPUT_DIR", str(tmp_path))
    (tmp_path / "main.log").write_text("! Undefined control sequence.\n")
    with patch("src.tools.lualatex_runner.subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "lualatex")
        with pytest.raises(CompilationError) as exc_info:
            lualatex_runner_tool._run(tex_file="main.tex", passes=1, run_biber=False)
    assert "SkillOpt" in str(exc_info.value)


@pytest.mark.skipif(shutil.which("lualatex") is None, reason="lualatex not installed")
class TestLualatexIntegration:
    def test_minimal_tex_compiles_successfully(self, tmp_path, monkeypatch):
        monkeypatch.setattr(settings, "OUTPUT_DIR", str(tmp_path))
        tex_file = tmp_path / "minimal.tex"
        tex_file.write_text(
            "\\documentclass{article}\n\\begin{document}\nHello.\n\\end{document}\n"
        )
        result = lualatex_runner_tool._run(
            tex_file=str(tex_file), passes=2, run_biber=False
        )
        assert result.get("success") is True

    def test_invalid_tex_raises_compilation_error(self, tmp_path, monkeypatch):
        monkeypatch.setattr(settings, "OUTPUT_DIR", str(tmp_path))
        tex_file = tmp_path / "broken.tex"
        tex_file.write_text(
            "\\documentclass{article}\n\\begin{document}\n"
            "\\UNDEFINED\n\\end{document}\n"
        )
        with pytest.raises(CompilationError):
            lualatex_runner_tool._run(
                tex_file=str(tex_file), passes=2, run_biber=False
            )
