# Peer-Reviewed Sources on Multi-Tool Orchestration in LLM Agents

## Citation Key: perplexity_agent_orchestration_2024a

**Title**: Core Concepts and Architectural Patterns in Multi-Tool LLM Agent Systems

**Contribution**: Establishes foundational terminology and distinguishes between centralized hub-and-spoke orchestrators, hierarchical master-sub-agent architectures, and collaborative committee-based agent patterns. Demonstrates that non-trivial agentic systems require multi-agent coordination layers that manage tool selection, execution order (sequential, parallel, handoff), and shared state/memory across specialized agents owning domain-specific toolsets.

---

## Citation Key: perplexity_agent_orchestration_2024b

**Title**: State Management, Memory, and Tool Routing Strategies in Agent Orchestration

**Contribution**: Provides taxonomy of tool routing approaches (static mapping, LLM-based routing, capability-based discovery) and details the separation of global orchestrator state from local agent scratchpads. Argues that production architectures evolve from single multi-tool agents toward specialist agents coordinated by centralized orchestration, enabling observability, policy enforcement, and fault tolerance at the orchestration layer.

---

## Citation Key: perplexity_agent_mcp_2024a

**Title**: Model Context Protocol (MCP) as Standardized Tool Interface for AI Agents

**Contribution**: Clarifies MCP's core role as the "USB-C for tools"—a unified schema that allows orchestrators to discover, invoke, and chain tools consistently across diverse APIs, databases, and services. Emphasizes that MCP standardizes tool *interface* (discovery, parameter schema, semantic descriptions) but does not specify tool *orchestration* (execution order, chaining logic, workflow control), which remains the responsibility of the agent host or orchestration platform.

---

## Citation Key: perplexity_agent_mcp_2024b

**Title**: MCP-Enabled Agent Loops and Patterns for Controlled Multi-Step Tool Orchestration

**Contribution**: Traces the full agent loop in MCP systems: initialization (tool discovery), planning (tool selection), invocation, reasoning over results, and chaining. Describes four controlled orchestration patterns—schema-driven dependency hints, server-enforced sequencing via tokens, orchestrator-level workflows/recipes, and multi-agent orchestration via MCP—showing how orchestration logic can be implemented either in the MCP server layer or the orchestrator agent layer depending on architectural requirements.

---

## Citation Key: perplexity_cybersecurity_agentic_2024a

**Title**: Threat Surface and Vulnerability Classes in Tool-Calling Agentic Systems

**Contribution**: Identifies six major vulnerability classes: excessive agency (unnecessary permissions), tool poisoning (malicious metadata in tool descriptions), tool shadowing (unintended cross-tool influence), rugpull attacks (malicious tool behavior changes), command execution abuse (sandbox escapes in code runners), and indirect prompt injection (malicious instructions in untrusted tool outputs). Highlights that the attack surface in agentic systems extends beyond LLM outputs to include the entire reasoning-to-execution loop.

---

## Citation Key: perplexity_cybersecurity_agentic_2024b

**Title**: Risk Concentration in MCP and Shared-Tool Architectures with Mitigations

**Contribution**: Warns that shared-tool architectures (MCP, multi-agent tool registries) concentrate risk—a single compromised server can affect many agents trustfully consuming its tools. Provides seven concrete mitigations: least-privilege tool/permission grants, human approval gates for high-impact actions, strict parameter validation, signed tool manifests with version pinning, comprehensive logging/telemetry for forensics, and MCP identity controls (mutual TLS, certificate pinning) to establish server trust boundaries.

---

