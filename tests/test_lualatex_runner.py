import shutil
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.config import settings
from src.tools.lualatex_runner import (
    CompilationError,
    LualatexRunnerInput,
    lualatex_runner_tool,
)


def test_compilation_error_is_exception_subclass():
    assert issubclass(CompilationError, Exception)


def test_log_parser_detects_error_line(tmp_path):
    log = tmp_path / "main.log"
    log.write_text("! LaTeX Error: File not found\n")
    errors = lualatex_runner_tool._parse_log(log)
    assert len(errors) > 0


def test_log_parser_clean_log_returns_empty_list(tmp_path):
    log = tmp_path / "main.log"
    log.write_text("This is LuaTeX, Version 1.16\n")
    errors = lualatex_runner_tool._parse_log(log)
    assert errors == []


def test_log_parser_detects_undefined_control_sequence(tmp_path):
    log = tmp_path / "main.log"
    log.write_text("! Undefined control sequence.\n")
    errors = lualatex_runner_tool._parse_log(log)
    assert len(errors) > 0


def test_log_parser_ignores_info_lines(tmp_path):
    log = tmp_path / "main.log"
    log.write_text("This is LuaTeX, Version 1.16\nDocument Class: article 2023/05/17\n")
    errors = lualatex_runner_tool._parse_log(log)
    assert errors == []


def test_build_cmd_contains_nonstopmode():
    cmd = lualatex_runner_tool._build_cmd("main.tex")
    assert "--interaction=nonstopmode" in cmd


def test_build_cmd_contains_output_directory_flag():
    cmd = lualatex_runner_tool._build_cmd("main.tex")
    assert any(s.startswith("--output-directory=") for s in cmd)


def test_build_cmd_contains_tex_filename():
    cmd = lualatex_runner_tool._build_cmd("main.tex")
    assert "main.tex" in cmd


def test_build_cmd_first_element_is_lualatex_bin():
    cmd = lualatex_runner_tool._build_cmd("main.tex")
    assert cmd[0] == settings.LUALATEX_BIN


def test_tool_name_attribute():
    assert lualatex_runner_tool.name == "lualatex_runner"


def test_default_passes_is_three():
    inp = LualatexRunnerInput(tex_file="main.tex")
    assert inp.passes == 3


def test_default_run_biber_is_true():
    inp = LualatexRunnerInput(tex_file="main.tex")
    assert inp.run_biber is True


def test_build_biber_cmd_contains_biber_bin():
    cmd = lualatex_runner_tool._build_biber_cmd("main")
    assert cmd[0] == settings.BIBER_BIN


def test_build_biber_cmd_contains_stem():
    cmd = lualatex_runner_tool._build_biber_cmd("main")
    assert "main" in cmd


def test_biber_called_between_lualatex_passes(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "OUTPUT_DIR", str(tmp_path))
    (tmp_path / "main.log").write_text("This is LuaTeX\n")
    with patch("src.tools.lualatex_runner.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        lualatex_runner_tool._run(tex_file="main.tex", passes=2, run_biber=True)
    cmds = [c.args[0] for c in mock_run.call_args_list]
    assert cmds[0][0] == settings.LUALATEX_BIN
    assert cmds[1][0] == settings.BIBER_BIN
    assert cmds[2][0] == settings.LUALATEX_BIN


def test_biber_skipped_when_run_biber_false(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "OUTPUT_DIR", str(tmp_path))
    (tmp_path / "main.log").write_text("This is LuaTeX\n")
    with patch("src.tools.lualatex_runner.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        lualatex_runner_tool._run(tex_file="main.tex", passes=2, run_biber=False)
    biber_calls = [
        c for c in mock_run.call_args_list if c.args[0][0] == settings.BIBER_BIN
    ]
    assert len(biber_calls) == 0


def test_hitl_gate_prompts_when_enabled(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "OUTPUT_DIR", str(tmp_path))
    monkeypatch.setattr(settings, "HITL_ENABLED", True)
    (tmp_path / "main.log").write_text("This is LuaTeX\n")
    with patch("src.tools.lualatex_runner.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        with patch("builtins.input", return_value="Y") as mock_input:
            lualatex_runner_tool._run(tex_file="main.tex", passes=1, run_biber=False)
            mock_input.assert_called_once()


def test_hitl_gate_aborts_when_user_declines(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "OUTPUT_DIR", str(tmp_path))
    monkeypatch.setattr(settings, "HITL_ENABLED", True)
    (tmp_path / "main.log").write_text("This is LuaTeX\n")
    with (
        patch("src.tools.lualatex_runner.subprocess.run"),
        patch("builtins.input", return_value="n"),
        pytest.raises(RuntimeError, match="HITL gate"),
    ):
        lualatex_runner_tool._run(tex_file="main.tex", passes=1, run_biber=False)


def test_hitl_gate_skipped_when_disabled(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "OUTPUT_DIR", str(tmp_path))
    monkeypatch.setattr(settings, "HITL_ENABLED", False)
    (tmp_path / "main.log").write_text("This is LuaTeX\n")
    with patch("src.tools.lualatex_runner.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        with patch("builtins.input") as mock_input:
            lualatex_runner_tool._run(tex_file="main.tex", passes=1, run_biber=False)
            mock_input.assert_not_called()


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
        tex_file: Path = tmp_path / "minimal.tex"
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
            "\\documentclass{article}\n\\begin{document}\n\\UNDEFINED\n\\end{document}\n"
        )
        with pytest.raises(CompilationError):
            lualatex_runner_tool._run(
                tex_file=str(tex_file), passes=2, run_biber=False
            )
