"""Lightweight A2A (Agent-to-Agent) protocol — mocks the Linux Foundation A2A standard.

Enables horizontal interoperability alongside our vertical MCP server:
- MCP  (vertical):  external callers → our tools  (top-down)
- A2A  (horizontal): our ManagerAgent ↔ peer agents on other nodes (peer-to-peer)

In production, `delegate_task` would POST to `card.endpoint` over HTTPS and
poll `GET /tasks/{task_id}` until status != "running".  Here the network call
is mocked so the architecture can be validated without external dependencies.
"""

import uuid
from dataclasses import dataclass, field


class A2AError(Exception):
    """Raised when an A2A operation fails (agent not found, delegation error)."""


@dataclass
class AgentCard:
    """External agent manifest — describes identity, endpoint, and capabilities."""

    agent_id: str
    endpoint: str  # e.g. "https://compiler-agent.acme.com/a2a"
    capabilities: list[str]
    protocol_version: str = "1.0"


@dataclass
class A2ATask:
    """Unit of work passed between agents via the A2A protocol."""

    description: str
    payload: dict
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "pending"  # pending | running | done | failed
    delegator_id: str = "manager"


class A2AProtocol:
    """Registry and dispatcher for inter-agent task delegation.

    Usage::

        proto = A2AProtocol()
        proto.register_agent(AgentCard(
            agent_id="ext-compiler",
            endpoint="https://compiler.acme.com/a2a",
            capabilities=["compile", "validate"],
        ))
        agents = proto.discover_agents(capability="compile")
        task   = A2ATask(description="Compile main.tex", payload={"file": "main.tex"})
        result = proto.delegate_task(task, target_agent_id="ext-compiler")
        # result.status == "done"
    """

    def __init__(self) -> None:
        self._registry: dict[str, AgentCard] = {}

    def register_agent(self, card: AgentCard) -> None:
        """Register an external agent by its card."""
        self._registry[card.agent_id] = card

    def list_agent_ids(self) -> list[str]:
        """Return IDs of all registered agents."""
        return list(self._registry.keys())

    def discover_agents(self, capability: str) -> list[AgentCard]:
        """Return all registered agents that advertise *capability*."""
        return [c for c in self._registry.values() if capability in c.capabilities]

    def delegate_task(self, task: A2ATask, target_agent_id: str) -> A2ATask:
        """Delegate *task* to the agent identified by *target_agent_id*.

        Raises:
            A2AError: if *target_agent_id* has not been registered.
        """
        if target_agent_id not in self._registry:
            raise A2AError(
                f"Agent {target_agent_id!r} is not registered. "
                "Call register_agent() first."
            )
        card = self._registry[target_agent_id]
        task.status = "running"
        task.payload["result"] = (
            f"[MOCK A2A] '{task.description}' completed"
            f" by agent '{card.agent_id}' at {card.endpoint}"
        )
        task.status = "done"
        return task


# Module-level singleton — use this in agents rather than constructing new instances.
a2a_protocol = A2AProtocol()
