"""Red-team: prompt injection and path traversal attacks."""

import pytest

from src.config import settings
from src.tools.markdown_converter import markdown_converter_tool


class TestPromptInjectionBlocked:
    """Attacker injects malicious strings into md_path / tex_path parameters.

    Defence: MarkdownConverterTool._validate_path() — raises ValueError.
    """

    def test_dot_dot_traversal_to_etc_passwd_blocked(self):
        with pytest.raises(ValueError, match="escapes"):
            markdown_converter_tool._validate_path("../../etc/passwd")

    def test_single_parent_hop_to_env_blocked(self):
        with pytest.raises(ValueError, match="escapes"):
            markdown_converter_tool._validate_path("../secrets/.env")

    def test_absolute_path_injection_to_shadow_blocked(self):
        with pytest.raises(ValueError, match="escapes"):
            markdown_converter_tool._validate_path("/etc/shadow")

    def test_deep_traversal_six_hops_blocked(self):
        with pytest.raises(ValueError, match="escapes"):
            markdown_converter_tool._validate_path("a/b/../../../../../../../etc/hosts")

    def test_double_slash_absolute_path_blocked(self):
        with pytest.raises(ValueError, match="escapes"):
            markdown_converter_tool._validate_path("//etc/passwd")

    def test_null_byte_injection_in_path_blocked(self):
        with pytest.raises((ValueError, TypeError)):
            markdown_converter_tool._validate_path("innocent\x00../../etc/passwd")

    def test_valid_path_within_output_dir_is_accepted(self, monkeypatch, tmp_path):
        monkeypatch.setattr(settings, "OUTPUT_DIR", str(tmp_path))
        result = markdown_converter_tool._validate_path("chapters/ch1.md")
        assert result.is_relative_to(tmp_path)
