from pathlib import Path
from unittest.mock import patch

import pytest

from src.crew import PublisherCrew, _load_skill

pytestmark = pytest.mark.usefixtures("mock_llm_creation")

_SKILL_NAMES = [
    "manager",
    "perplexity-research",
    "academic-outline",
    "hebrew-academic-writing",
    "lualatex-bidi",
    "matplotlib-tikz",
    "lualatex-build",
    "latex_expert",
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


def test_publisher_crew_init_loads_eight_skills():
    with patch("src.crew._load_skill", return_value="dummy") as mock_load:
        PublisherCrew()
    assert mock_load.call_count == 8


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
    assert crew.compiler_agent.backstory == (
        skill_map["lualatex-build"] + "\n\n" + skill_map["latex_expert"]
    )


def test_no_agent_backstory_is_hardcoded_python_string():
    forbidden = ["You are a", "Your role is", "You specialize in"]
    for filepath in _AGENT_FILES:
        text = Path(filepath).read_text()
        for phrase in forbidden:
            assert phrase not in text, (
                f"{filepath} contains hardcoded backstory phrase: {phrase!r}"
            )


# ── Task / agent counts ───────────────────────────────────────────────────────


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
