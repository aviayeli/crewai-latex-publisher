# Research Index — Multi-Tool Orchestration in LLM Agents

## Citation Key Reference

| Citation Key | One-Line Description |
|---|---|
| `Anthropic_2024_AgentArchitecture` | Multi-tool orchestration as a coordination layer managing which tools run, in what order; separates orchestrator/router, specialized agents, shared state, and evaluation guardrails. |
| `Anthropic_2024_MCPProtocol` | Model Context Protocol (MCP): open standard for exposing tools, data, and prompts to LLMs; achieves N+M integration complexity by standardizing tool discovery and invocation across clients. |
| `Anthropic_Palo_Alto_2024_PromptInjectionSecurity` | Agentic security threats from prompt injection and jailbreak attacks that leverage tool orchestration, multi-step reasoning, and multi-agent ecosystems for privilege escalation and data exfiltration. |
| `Stanford_MIT_2023_HierarchicalMultiAgentRL` | Hierarchical orchestration combines RL, symbolic planning, and decomposition; planning agents construct execution plans for specialist agents with continuous learning and feedback loops. |
| `CrewAI_2024_HierarchicalDelegation` | Manager-agent pattern in CrewAI: manager decomposes tasks, delegates to workers, aggregates results; optional custom managers; Flow-based alternative for full delegation control. |
| `OpenAI_2024_AgentsMCPIntegration` | OpenAI Agents SDK integrates MCP servers as tools via multiple transports (hosted, HTTP, SSE, stdio) for seamless multi-tool agent orchestration across frameworks. |

## Full Descriptions

For detailed one-paragraph descriptions of each source's contribution, see [wiki/sources.md](./sources.md).

## Research Scope

This research corpus addresses:
- **AI Agent Architecture:** orchestrator/router patterns, specialized agents, shared state, and guardrails
- **MCP Protocol:** standardized tool exposure, client–server architecture, capabilities discovery, interoperability
- **Multi-Tool Orchestration:** dynamic planning vs. code-based control flow, hierarchical vs. sequential/parallel processes
- **Cybersecurity in Agentic Systems:** direct/indirect prompt injection, privilege escalation, defensive patterns (least-privilege tooling, human-in-the-loop, behavioral analytics, adversarial testing)
- **Hierarchical Coordination:** RL-based policy learning, multi-agent collaboration, task decomposition, planning agents
- **Production Frameworks:** CrewAI, OpenAI Agents SDK, LangGraph, Semantic Kernel

---

*Raw research data (unprocessed Perplexity output) is archived at [raw/research_raw.md](../raw/research_raw.md) for audit purposes.*