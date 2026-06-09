import pytest
from pydantic import ValidationError

from src.tools.latex_writer import LatexWriterInput, latex_writer_tool


def test_tool_name_attribute():
    assert latex_writer_tool.name == "latex_writer"


def test_args_schema_has_path_field():
    assert "path" in LatexWriterInput.model_fields


def test_args_schema_has_content_field():
    assert "content" in LatexWriterInput.model_fields


def test_args_schema_has_mode_field():
    assert "mode" in LatexWriterInput.model_fields


def test_write_creates_file(tmp_output_dir):
    latex_writer_tool._run(
        path="chapters/ch1.tex", content="\\chapter{Test}", mode="write"
    )
    out = tmp_output_dir / "chapters" / "ch1.tex"
    assert out.exists()
    assert out.read_text(encoding="utf-8") == "\\chapter{Test}"


def test_write_overwrites_existing_file(tmp_output_dir):
    latex_writer_tool._run(path="chapters/ch1.tex", content="first", mode="write")
    latex_writer_tool._run(path="chapters/ch1.tex", content="second", mode="write")
    got = (tmp_output_dir / "chapters" / "ch1.tex").read_text(encoding="utf-8")
    assert got == "second"


def test_append_adds_content(tmp_output_dir):
    latex_writer_tool._run(path="chapters/ch1.tex", content="hello ", mode="write")
    latex_writer_tool._run(path="chapters/ch1.tex", content="world", mode="append")
    got = (tmp_output_dir / "chapters" / "ch1.tex").read_text(encoding="utf-8")
    assert got == "hello world"


def test_append_to_nonexistent_creates_file(tmp_output_dir):
    latex_writer_tool._run(path="chapters/new.tex", content="content", mode="append")
    got = (tmp_output_dir / "chapters" / "new.tex").read_text(encoding="utf-8")
    assert got == "content"


def test_path_traversal_rejected_dotdot(tmp_output_dir):
    with pytest.raises(ValueError):
        latex_writer_tool._run(path="../../../etc/passwd", content="x", mode="write")


def test_path_traversal_rejected_absolute_path(tmp_output_dir):
    with pytest.raises(ValueError):
        latex_writer_tool._run(path="/etc/passwd", content="x", mode="write")


def test_creates_parent_directories(tmp_output_dir):
    latex_writer_tool._run(
        path="chapters/sub/deep/ch1.tex", content="x", mode="write"
    )
    assert (tmp_output_dir / "chapters" / "sub" / "deep" / "ch1.tex").exists()


def test_utf8_encoding_hebrew(tmp_output_dir):
    hebrew = "שלום עולם"
    latex_writer_tool._run(path="chapters/ch_heb.tex", content=hebrew, mode="write")
    result = (tmp_output_dir / "chapters" / "ch_heb.tex").read_text(encoding="utf-8")
    assert result == hebrew


def test_return_value_contains_path(tmp_output_dir):
    result = latex_writer_tool._run(
        path="chapters/ch1.tex", content="x", mode="write"
    )
    assert "ch1.tex" in result


def test_write_empty_string(tmp_output_dir):
    latex_writer_tool._run(path="chapters/empty.tex", content="", mode="write")
    out = tmp_output_dir / "chapters" / "empty.tex"
    assert out.exists()
    assert out.stat().st_size == 0


def test_mode_invalid_raises_validation_error():
    with pytest.raises((ValidationError, ValueError)):
        LatexWriterInput(path="chapters/ch1.tex", content="x", mode="overwrite")


# ── prepend mode ──────────────────────────────────────────────────────────────


def test_prepend_inserts_before_existing_content(tmp_output_dir):
    latex_writer_tool._run(path="chapters/ch1.tex", content="BODY\n", mode="write")
    latex_writer_tool._run(
        path="chapters/ch1.tex", content="HEADER\n", mode="prepend"
    )
    got = (tmp_output_dir / "chapters" / "ch1.tex").read_text(encoding="utf-8")
    assert got == "HEADER\nBODY\n"


def test_prepend_to_nonexistent_creates_file(tmp_output_dir):
    latex_writer_tool._run(
        path="chapters/new.tex", content="prefix", mode="prepend"
    )
    got = (tmp_output_dir / "chapters" / "new.tex").read_text(encoding="utf-8")
    assert got == "prefix"


def test_prepend_mode_valid_in_schema():
    obj = LatexWriterInput(path="chapters/ch1.tex", content="x", mode="prepend")
    assert obj.mode == "prepend"


# ── templates directory access ────────────────────────────────────────────────


def test_templates_dir_write_allowed(tmp_output_dir, tmp_path, monkeypatch):
    # OUTPUT_DIR = tmp_path, so ../templates/ resolves to tmp_path.parent/templates/
    templates_dir = tmp_path.parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("src.tools.latex_writer.settings.TEMPLATES_DIR",
                        str(templates_dir))
    result = latex_writer_tool._run(
        path="../templates/preamble.tex", content="\\usepackage{tikz}", mode="write"
    )
    assert (templates_dir / "preamble.tex").exists()
    assert "preamble.tex" in result


def test_path_outside_both_dirs_rejected(tmp_output_dir, tmp_path, monkeypatch):
    templates_dir = tmp_path.parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("src.tools.latex_writer.settings.TEMPLATES_DIR",
                        str(templates_dir))
    with pytest.raises(ValueError):
        latex_writer_tool._run(path="../../etc/passwd", content="x", mode="write")
