from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from crewai import Process

from src.config import settings
from src.crew import PublisherCrew, _load_skill

_SKILL_NAMES = [
    "manager",
    "perplexity-research",
    "academic-outline",
    "hebrew-academic-writing",
    "lualatex-bidi",
    "matplotlib-tikz",
    "lualatex-build",
]

_AGENT_FILES = [
    "src/agents/manager_agent.py",
    "src/agents/researcher_agent.py",
    "src/agents/outline_agent.py",
    "src/agents/content_agent.py",
    "src/agents/bidi_agent.py",
    "src/agents/figure_agent.py",
    "src/agents/compiler_agent.py",
]


@pytest.fixture(autouse=True)
def mock_llm_creation():
    mock = MagicMock()
    mock.model = settings.LLM_MODEL
    with patch("crewai.agent.core.create_llm", return_value=mock):
        yield


# ── _load_skill ───────────────────────────────────────────────────────────────


def test_load_skill_reads_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    skill_dir = tmp_path / "skills" / "test-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("test skill content")
    assert _load_skill("test-skill") == "test skill content"


def test_load_skill_missing_raises_file_not_found():
    with pytest.raises(FileNotFoundError):
        _load_skill("nonexistent-skill-xyz")


def test_load_skill_reads_from_skills_subdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    skill_dir = tmp_path / "skills" / "foo"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("foo content")
    assert _load_skill("foo") == "foo content"


# ── PublisherCrew construction ────────────────────────────────────────────────


def test_publisher_crew_init_loads_seven_skills():
    with patch("src.crew._load_skill", return_value="dummy") as mock_load:
        PublisherCrew()
    assert mock_load.call_count == 7


def test_all_agent_backstories_equal_skill_content():
    skill_map = {name: f"skill-{name}" for name in _SKILL_NAMES}
    with patch("src.crew._load_skill", side_effect=lambda n: skill_map[n]):
        crew = PublisherCrew()
    assert crew.manager_agent.backstory == skill_map["manager"]
    assert crew.researcher_agent.backstory == skill_map["perplexity-research"]
    assert crew.outline_agent.backstory == skill_map["academic-outline"]
    assert crew.content_agent.backstory == skill_map["hebrew-academic-writing"]
    assert crew.bidi_agent.backstory == skill_map["lualatex-bidi"]
    assert crew.figure_agent.backstory == skill_map["matplotlib-tikz"]
    assert crew.compiler_agent.backstory == skill_map["lualatex-build"]


def test_no_agent_backstory_is_hardcoded_python_string():
    forbidden = ["You are a", "Your role is", "You specialize in"]
    for filepath in _AGENT_FILES:
        text = Path(filepath).read_text()
        for phrase in forbidden:
            assert phrase not in text, (
                f"{filepath} contains hardcoded backstory phrase: {phrase!r}"
            )


def test_crew_has_exactly_eleven_tasks():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    all_tasks = (
        [crew.research_task, crew.outline_task]
        + crew.content_tasks
        + [crew.figure_task, crew.bidi_task, crew.compile_task]
    )
    assert len(all_tasks) == 11


def test_crew_has_exactly_seven_agents():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    agents = [
        crew.manager_agent,
        crew.researcher_agent,
        crew.outline_agent,
        crew.content_agent,
        crew.bidi_agent,
        crew.figure_agent,
        crew.compiler_agent,
    ]
    assert len(agents) == 7
    assert len({id(a) for a in agents}) == 7


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


def test_compile_task_context_contains_bidi_and_figure():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    assert crew.bidi_task in crew.compile_task.context
    assert crew.figure_task in crew.compile_task.context


# ── Agent settings ────────────────────────────────────────────────────────────


def test_all_agents_llm_matches_settings():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    all_agents = [
        crew.manager_agent,
        crew.researcher_agent,
        crew.outline_agent,
        crew.content_agent,
        crew.bidi_agent,
        crew.figure_agent,
        crew.compiler_agent,
    ]
    for agent in all_agents:
        assert agent.llm.model == settings.LLM_MODEL


def test_all_agents_max_retry_matches_settings():
    with patch("src.crew._load_skill", return_value="dummy"):
        crew = PublisherCrew()
    all_agents = [
        crew.manager_agent,
        crew.researcher_agent,
        crew.outline_agent,
        crew.content_agent,
        crew.bidi_agent,
        crew.figure_agent,
        crew.compiler_agent,
    ]
    for agent in all_agents:
        assert agent.max_retry_limit == settings.MAX_AGENT_RETRIES


def test_missing_skill_file_prevents_crew_init():
    with patch(
        "src.crew._load_skill",
        side_effect=FileNotFoundError("skills/manager/SKILL.md"),
    ):
        with pytest.raises(FileNotFoundError):
            PublisherCrew()


# ── Kickoff / Process ─────────────────────────────────────────────────────────


def test_kickoff_constructs_hierarchical_crew():
    with patch("src.crew._load_skill", return_value="dummy"):
        with patch("src.crew.Crew") as MockCrew:
            MockCrew.return_value.kickoff.return_value = "result"
            PublisherCrew().kickoff()
    assert MockCrew.call_args.kwargs["process"] == Process.hierarchical


def test_manager_agent_passed_as_kwarg():
    with patch("src.crew._load_skill", return_value="dummy"):
        with patch("src.crew.Crew") as MockCrew:
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
