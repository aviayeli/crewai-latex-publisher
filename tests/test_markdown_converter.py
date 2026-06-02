import shutil
from unittest.mock import patch

import pytest
from src.tools.markdown_converter import (
    MarkdownConverterInput,
    markdown_converter_tool,
)

from src.config import settings


def test_tool_name_attribute():
    assert markdown_converter_tool.name == "markdown_converter"


def test_args_schema_has_md_path_field():
    assert "md_path" in MarkdownConverterInput.model_fields


def test_args_schema_has_tex_path_field():
    assert "tex_path" in MarkdownConverterInput.model_fields


def test_path_traversal_md_rejected(tmp_output_dir):
    with pytest.raises(ValueError):
        markdown_converter_tool._run(
            md_path="../escape.md", tex_path="chapters/ch1.tex"
        )


def test_path_traversal_tex_rejected(tmp_output_dir):
    with pytest.raises(ValueError):
        markdown_converter_tool._run(
            md_path="chapters/ch1.md", tex_path="../../etc/evil.tex"
        )


def test_return_value_contains_output_path(tmp_output_dir):
    with patch("src.tools.markdown_converter.subprocess.run"):
        result = markdown_converter_tool._run(
            md_path="chapters/ch1.md", tex_path="chapters/ch1.tex"
        )
    assert "ch1.tex" in result


def test_pandoc_called_with_correct_flags(tmp_output_dir):
    with patch("src.tools.markdown_converter.subprocess.run") as mock_run:
        markdown_converter_tool._run(
            md_path="chapters/ch1.md", tex_path="chapters/ch1.tex"
        )
    cmd = mock_run.call_args.args[0]
    assert "-f" in cmd
    assert "markdown" in cmd
    assert "-t" in cmd
    assert "latex" in cmd
    assert "-o" in cmd


def test_pandoc_not_found_raises(tmp_output_dir):
    with patch.object(settings, "PANDOC_BIN", "nonexistent-binary-xyz"):
        with pytest.raises((FileNotFoundError, OSError)):
            markdown_converter_tool._run(
                md_path="chapters/ch1.md", tex_path="chapters/ch1.tex"
            )


@pytest.mark.skipif(shutil.which("pandoc") is None, reason="pandoc not installed")
class TestRealPandoc:
    def test_real_markdown_converts_to_tex(self, tmp_output_dir):
        md_file = tmp_output_dir / "chapters" / "test.md"
        md_file.write_text("# Hello\nThis is a test.", encoding="utf-8")
        markdown_converter_tool._run(
            md_path="chapters/test.md", tex_path="chapters/test.tex"
        )
        tex_file = tmp_output_dir / "chapters" / "test.tex"
        assert tex_file.exists()
        assert tex_file.stat().st_size > 0
