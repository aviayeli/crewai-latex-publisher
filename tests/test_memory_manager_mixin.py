"""Tests for MemoryManagerMixin — written before implementation (TDD mandate)."""
from src.utils.mixins import MemoryManagerMixin


class _Impl(MemoryManagerMixin):
    pass


class TestCompact:
    def test_empty_list_returns_empty_string(self):
        assert _Impl().compact([]) == ""

    def test_returns_string(self):
        result = _Impl().compact(["section A about deep learning"])
        assert isinstance(result, str) and len(result) > 0

    def test_section_count_in_output(self):
        result = _Impl().compact(["s1 text", "s2 text", "s3 text"])
        assert "3" in result

    def test_output_contains_digits(self):
        result = _Impl().compact(["hello world", "foo bar baz"])
        assert any(c.isdigit() for c in result)


class TestActiveContext:
    def test_within_window_unchanged(self):
        impl = _Impl()
        sections = ["s1", "s2", "s3"]
        assert impl.active_context(sections, window=3) == sections

    def test_exact_window_unchanged(self):
        impl = _Impl()
        assert impl.active_context(["s1", "s2"], window=2) == ["s1", "s2"]

    def test_overflow_produces_summary_plus_window(self):
        impl = _Impl()
        sections = ["s1", "s2", "s3", "s4", "s5"]
        result = impl.active_context(sections, window=2)
        assert len(result) == 3
        assert result[-2] == "s4"
        assert result[-1] == "s5"

    def test_summary_is_first_element(self):
        impl = _Impl()
        sections = ["alpha", "beta", "gamma", "delta"]
        result = impl.active_context(sections, window=1)
        assert len(result) == 2
        assert result[-1] == "delta"
        assert isinstance(result[0], str) and len(result[0]) > 0

    def test_empty_history_returns_empty(self):
        assert _Impl().active_context([], window=3) == []
