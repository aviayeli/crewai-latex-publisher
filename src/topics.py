"""Academic topic registry: menu definitions and progressive-disclosure routing.

Topics are indexed 15–18 to reflect their academic seminar position.
The user enters a positional choice (1–4); the menu shows the curriculum ID
([15]–[18]) as context.  Choices 1 & 3 route to the Deep Learning cluster;
choices 2 & 4 route to the Agent Architecture cluster.
"""

from dataclasses import dataclass

# ── Research cluster focus strings ────────────────────────────────────────────

_DL_FOCUS = (
    "Deep Learning, PyTorch, RNN/LSTM architectures,"
    " and sequential data processing"
)
_AGENT_FOCUS = (
    "AI Agent architecture, MCP protocol, multi-tool orchestration,"
    " and cybersecurity in agentic systems"
)

# ── Topic model ───────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Topic:
    """A selectable academic subject with its progressive-disclosure context."""

    display_id: int      # curriculum ID shown in the menu ([15]–[18])
    title: str           # full title passed to the crew as {topic}
    research_focus: str  # injected alongside title to guide the research agent


# ── Registry ──────────────────────────────────────────────────────────────────

TOPICS: tuple[Topic, ...] = (
    Topic(
        display_id=15,
        title=(
            "Sine Wave Extraction from Noisy Mixed Signals"
            " via Deep Learning (RNN/LSTM)"
        ),
        research_focus=_DL_FOCUS,
    ),
    Topic(
        display_id=16,
        title=(
            "Supply Chain Security in Agentic Ecosystems"
            " (ClawHavoc & SkillSieve)"
        ),
        research_focus=_AGENT_FOCUS,
    ),
    Topic(
        display_id=17,
        title="Benchmarking Transformers vs. xLSTM for Time-Series Forecasting",
        research_focus=_DL_FOCUS,
    ),
    Topic(
        display_id=18,
        title="The Evolution of Multi-Tool Orchestration in LLM Agents",
        research_focus=_AGENT_FOCUS,
    ),
)

# ── ASCII menu ────────────────────────────────────────────────────────────────

_BANNER = (
    "\n╔══════════════════════════════════════════════════╗\n"
    "║    LaTeX Academic Publisher — Topic Selection    ║\n"
    "╚══════════════════════════════════════════════════╝"
)

_VALID = {str(i): t for i, t in enumerate(TOPICS, start=1)}


def display_menu() -> None:
    """Print the numbered topic selection menu to stdout."""
    print(_BANNER)
    for i, topic in enumerate(TOPICS, start=1):
        print(f"  [{topic.display_id}]  ({i}) {topic.title}")
    print()


def select_topic() -> Topic:
    """Interactively prompt until the user enters a valid choice (1–4)."""
    display_menu()
    while True:
        choice = input("Select topic [1-4]: ").strip()
        if choice in _VALID:
            selected = _VALID[choice]
            print(f'\n  Selected: "{selected.title}"\n')
            return selected
        print(f"  Invalid choice {choice!r} — please enter 1, 2, 3, or 4.")
