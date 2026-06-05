"""Tests for the A2A (Agent-to-Agent) protocol implementation."""

import pytest

from src.orchestration.a2a_protocol import (
    A2AError,
    A2AProtocol,
    A2ATask,
    AgentCard,
    a2a_protocol,
)

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


# ── A2AProtocol.register_agent / list_agent_ids ───────────────────────────────


def test_register_agent_adds_id_to_registry():
    proto = A2AProtocol()
    card = AgentCard(
        agent_id="worker-1", endpoint="http://w.local/a2a", capabilities=["write"]
    )
    proto.register_agent(card)
    assert "worker-1" in proto.list_agent_ids()


def test_list_agent_ids_empty_on_fresh_protocol():
    proto = A2AProtocol()
    assert proto.list_agent_ids() == []


def test_register_multiple_agents_all_appear():
    proto = A2AProtocol()
    for i in range(3):
        proto.register_agent(
            AgentCard(
                agent_id=f"agent-{i}",
                endpoint=f"http://a{i}.local/a2a",
                capabilities=[],
            )
        )
    assert len(proto.list_agent_ids()) == 3


# ── A2AProtocol.discover_agents ───────────────────────────────────────────────


def test_discover_agents_returns_matching_card():
    proto = A2AProtocol()
    card = AgentCard(
        agent_id="compiler", endpoint="http://c.local/a2a", capabilities=["compile"]
    )
    proto.register_agent(card)
    results = proto.discover_agents(capability="compile")
    assert any(c.agent_id == "compiler" for c in results)


def test_discover_agents_returns_empty_for_unknown_capability():
    proto = A2AProtocol()
    assert proto.discover_agents(capability="does-not-exist") == []


def test_discover_agents_excludes_non_matching():
    proto = A2AProtocol()
    proto.register_agent(AgentCard(
        agent_id="researcher", endpoint="http://r.local/a2a", capabilities=["research"]
    ))
    results = proto.discover_agents(capability="compile")
    assert results == []


# ── A2AProtocol.delegate_task ─────────────────────────────────────────────────


def test_delegate_task_returns_task_with_done_status():
    proto = A2AProtocol()
    proto.register_agent(AgentCard(
        agent_id="ext-worker", endpoint="http://w.local/a2a", capabilities=["write"]
    ))
    task = A2ATask(description="Write ch7", payload={"chapter": 7})
    result = proto.delegate_task(task, target_agent_id="ext-worker")
    assert result.status == "done"


def test_delegate_task_populates_result_in_payload():
    proto = A2AProtocol()
    proto.register_agent(AgentCard(
        agent_id="ext-worker", endpoint="http://w.local/a2a", capabilities=["write"]
    ))
    task = A2ATask(description="Write ch7", payload={})
    result = proto.delegate_task(task, target_agent_id="ext-worker")
    assert "result" in result.payload


def test_delegate_task_result_mentions_agent_id():
    proto = A2AProtocol()
    proto.register_agent(AgentCard(
        agent_id="ext-compiler", endpoint="http://c.local/a2a", capabilities=["compile"]
    ))
    task = A2ATask(description="compile", payload={})
    result = proto.delegate_task(task, target_agent_id="ext-compiler")
    assert "ext-compiler" in result.payload["result"]


def test_delegate_to_unregistered_agent_raises_a2a_error():
    proto = A2AProtocol()
    task = A2ATask(description="orphan", payload={})
    with pytest.raises(A2AError, match="not registered"):
        proto.delegate_task(task, target_agent_id="ghost-agent")


def test_a2a_error_is_exception_subclass():
    assert issubclass(A2AError, Exception)


# ── module-level singleton ────────────────────────────────────────────────────


def test_a2a_protocol_singleton_is_protocol_instance():
    assert isinstance(a2a_protocol, A2AProtocol)
