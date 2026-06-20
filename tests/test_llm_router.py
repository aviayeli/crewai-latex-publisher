"""Tests for LLMRouter and LocalLLMStub (TDD — written before implementation)."""
from unittest.mock import patch

from src.utils.llm_router import LLMRouter, LocalLLMStub, TaskComplexity


class TestTaskComplexity:
    def test_has_simple_and_complex(self):
        assert TaskComplexity.SIMPLE is not None
        assert TaskComplexity.COMPLEX is not None

    def test_values_are_strings(self):
        assert isinstance(TaskComplexity.SIMPLE.value, str)
        assert isinstance(TaskComplexity.COMPLEX.value, str)


class TestLocalLLMStub:
    def test_default_model_is_ollama(self):
        stub = LocalLLMStub()
        assert "ollama" in stub.model or "llama" in stub.model.lower()

    def test_custom_model_stored(self):
        stub = LocalLLMStub(model="ollama/mistral")
        assert stub.model == "ollama/mistral"

    def test_repr_includes_class_name(self):
        assert "LocalLLMStub" in repr(LocalLLMStub())


class TestLLMRouter:
    def test_inherits_finops_mixin(self):
        from src.utils.mixins import FinOpsMixin
        assert issubclass(LLMRouter, FinOpsMixin)

    def test_complex_routes_to_smart_llm(self):
        router = LLMRouter()
        with (
            patch("src.utils.llm_router.settings") as mock_s,
            patch("src.utils.llm_router.build_llm_smart", return_value="smart") as mock,
        ):
            mock_s.DRY_RUN = False
            result = router.route(TaskComplexity.COMPLEX)
            mock.assert_called_once()
            assert result == "smart"

    def test_simple_routes_to_local_stub(self):
        router = LLMRouter()
        with patch("src.utils.llm_router.settings") as mock_s:
            mock_s.DRY_RUN = False
            result = router.route(TaskComplexity.SIMPLE)
        assert isinstance(result, LocalLLMStub)

    def test_dry_run_overrides_to_fast(self):
        router = LLMRouter()
        fast_patch = patch("src.utils.llm_router.build_llm_fast", return_value="fast")
        with patch("src.utils.llm_router.settings") as mock_s, fast_patch as mock_fast:
            mock_s.DRY_RUN = True
            result = router.route(TaskComplexity.COMPLEX)
            mock_fast.assert_called_once()
            assert result == "fast"

    def test_route_tracks_call_count(self):
        router = LLMRouter()
        with (
            patch("src.utils.llm_router.settings") as mock_s,
            patch("src.utils.llm_router.build_llm_smart", return_value="s"),
        ):
            mock_s.DRY_RUN = False
            router.route(TaskComplexity.COMPLEX)
            router.route(TaskComplexity.COMPLEX)
        assert router.call_count == 2


class TestLLMRouterClassify:
    def test_format_keyword_is_simple(self):
        assert LLMRouter().classify("format the bibliography") == TaskComplexity.SIMPLE

    def test_fix_keyword_is_simple(self):
        assert LLMRouter().classify("fix LaTeX syntax errors") == TaskComplexity.SIMPLE

    def test_spell_keyword_is_simple(self):
        assert LLMRouter().classify("spell check the abstract") == TaskComplexity.SIMPLE

    def test_syntax_keyword_is_simple(self):
        result = LLMRouter().classify("validate syntax in chapter 2")
        assert result == TaskComplexity.SIMPLE

    def test_structure_is_complex(self):
        result = LLMRouter().classify("structure the paper outline")
        assert result == TaskComplexity.COMPLEX

    def test_research_is_complex(self):
        result = LLMRouter().classify("analyze research findings")
        assert result == TaskComplexity.COMPLEX
