"""Tests for A2A protocol model classes: AgentCard and A2ATask."""

from src.orchestration.a2a_protocol import A2ATask, AgentCard

# ── AgentCard ─────────────────────────────────────────────────────────────────


def test_agent_card_stores_agent_id():
    card = AgentCard(
        agent_id="ext-compiler",
        endpoint="http://compiler.acme.com/a2a",
        capabilities=["compile"],
    )
    assert card.agent_id == "ext-compiler"


def test_agent_card_default_protocol_version_is_1_0():
    card = AgentCard(agent_id="a", endpoint="http://a.local/a2a", capabilities=[])
    assert card.protocol_version == "1.0"


# ── A2ATask ───────────────────────────────────────────────────────────────────


def test_a2a_task_default_status_is_pending():
    task = A2ATask(description="compile", payload={})
    assert task.status == "pending"


def test_a2a_task_has_auto_generated_uuid():
    t1 = A2ATask(description="task 1", payload={})
    t2 = A2ATask(description="task 2", payload={})
    assert t1.task_id != t2.task_id


def test_a2a_task_task_id_is_non_empty_string():
    task = A2ATask(description="x", payload={})
    assert isinstance(task.task_id, str) and task.task_id


def test_a2a_task_default_delegator_is_manager():
    task = A2ATask(description="x", payload={})
    assert task.delegator_id == "manager"
