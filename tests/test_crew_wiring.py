from unittest.mock import MagicMock, patch

import pytest
from crewai import Process

from src.config import settings
from src.crew import PublisherCrew

pytestmark = pytest.mark.usefixtures("mock_llm_creation")


# ── Task context wiring ───────────────────────────────────────────────────────


def test_content_tasks_each_have_outline_in_context():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    for task in crew.content_tasks:
        assert crew.outline_task in task.context


def test_bidi_task_context_contains_all_six_content_tasks():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert len(crew.bidi_task.context) == 6


def test_figure_task_context_contains_outline_task():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert crew.outline_task in crew.figure_task.context


def test_compile_task_context_contains_abstract_and_figure_embed():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert crew.abstract_task in crew.compile_task.context
    assert crew.figure_embed_task in crew.compile_task.context


def test_abstract_task_context_contains_bidi_task():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert crew.bidi_task in crew.abstract_task.context


def test_figure_embed_task_context_contains_figure_task():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert crew.figure_task in crew.figure_embed_task.context


# ── Agent settings ────────────────────────────────────────────────────────────


def test_fast_tier_agents_use_fast_builder():
    """Outline, Compiler, Manager must call build_llm_fast — not the default builder."""
    # Return a model-name string so crewai Agent pydantic validation passes.
    _fast = MagicMock(return_value=settings.LLM_MODEL_FAST)
    with (
        patch("src.crew._load_skill", return_value="dummy"),
        patch("src.agents.outline_agent.build_llm_fast", _fast),
        patch("src.agents.compiler_agent.build_llm_fast", _fast),
        patch("src.agents.manager_agent.build_llm_fast", _fast),
    ):
        PublisherCrew()
    assert _fast.call_count == 3


def test_smart_tier_agents_use_smart_builder():
    """ContentWriter and BiDiValidator must call build_llm_smart."""
    _smart = MagicMock(return_value=settings.LLM_MODEL_SMART)
    with (
        patch("src.crew._load_skill", return_value="dummy"),
        patch("src.agents.content_agent.build_llm_smart", _smart),
        patch("src.agents.bidi_agent.build_llm_smart", _smart),
    ):
        PublisherCrew()
    assert _smart.call_count == 2


def test_all_agents_max_retry_matches_settings():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    all_agents = [
        crew.manager_agent, crew.researcher_agent, crew.outline_agent,
        crew.content_agent, crew.bidi_agent, crew.figure_agent,
        crew.compiler_agent,
    ]
    for agent in all_agents:
        assert agent.max_retry_limit == settings.MAX_AGENT_RETRIES


def test_all_agents_max_iter_matches_settings():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    all_agents = [
        crew.manager_agent, crew.researcher_agent, crew.outline_agent,
        crew.content_agent, crew.bidi_agent, crew.figure_agent,
        crew.compiler_agent,
    ]
    for agent in all_agents:
        assert agent.max_iter == settings.MAX_ITER


def test_missing_skill_file_prevents_crew_init():
    with (
        patch(
            "src.crew._load_skill",
            side_effect=FileNotFoundError("skills/manager/SKILL.md"),
        ),
        pytest.raises(FileNotFoundError),
    ):
        PublisherCrew()


# ── Kickoff / Process ─────────────────────────────────────────────────────────


def test_kickoff_constructs_hierarchical_crew():
    with (
        patch("src.crew._load_skill", return_value="dummy"),
        patch("src.crew.Crew") as MockCrew,
    ):
        MockCrew.return_value.kickoff.return_value = "result"
        PublisherCrew().kickoff()
    assert MockCrew.call_args.kwargs["process"] == Process.hierarchical


def test_manager_agent_passed_as_kwarg():
    with (
        patch("src.crew._load_skill", return_value="dummy"),
        patch("src.crew.Crew") as MockCrew,
    ):
        MockCrew.return_value.kickoff.return_value = "result"
        crew = PublisherCrew()
        crew.kickoff()
    kwargs = MockCrew.call_args.kwargs
    assert "manager_agent" in kwargs
    assert crew.manager_agent not in kwargs.get("agents", [])


def test_manager_agent_allow_delegation_true():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert crew.manager_agent.allow_delegation is True


# ── Research / outline dependency ─────────────────────────────────────────────


def test_research_task_has_no_context():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert not crew.research_task.context


def test_outline_task_context_contains_research_task():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert crew.research_task in crew.outline_task.context
