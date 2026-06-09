# Raw Perplexity Research Output

## Query 1: Multi-tool LLM agent architectures
Multi‑tool LLM agent architectures use one or more **orchestrator agents** that break a goal into sub‑tasks, route each sub‑task to specialized tool‑using agents (search, RAG, APIs, code, etc.), manage shared state/memory, and then synthesize results into a final answer.

### Core Concepts
- **Agent**: An LLM plus tools (functions/APIs, RAG, code execution, DBs), policy (what it is allowed to do), and local memory/state.
- **Orchestration**: Logic that decides which agent or tool to call, in what order (sequential, parallel, handoff), with what state/context.
- **Multi‑tool vs multi‑agent**: Multi‑tool single agent means one agent chooses among many tools. Multi‑agent means several agents coordinated by an orchestrator.

### High-level Architectural Patterns
1. **Centralized "orchestrator" (hub‑and‑spoke)**: One orchestrator agent keeps global state and decides which specialist agent/tool to call next.
2. **Hierarchical (master + sub‑agents)**: Master agent handles the mission and spawns sub‑agents with tools tailored to sub‑domains.
3. **Collaborative / committee agents**: Multiple peer agents work together and negotiate or vote on outputs instead of having a single controller.

### Orchestration Flow Patterns
- **Sequential**: Agents/tools invoked one after another, passing updated state along the chain.
- **Concurrent (parallel)**: Orchestrator spawns multiple agents in parallel on independent sub‑tasks, then aggregates results.
- **Handoff / relay**: Agent A completes its role and explicitly hands off to Agent B.
- **Group chat / mediated conversation**: Multiple agents interact in a shared conversation; a mediator decides whose turn it is next.

### State, Memory, and Tool Routing
- **Global state**: Maintained by the orchestrator (user goal, task graph, message history, artifacts).
- **Local state**: Specific to each agent (internal scratchpad, tool‑specific cache).
- **Tool routing strategies**: Static routing, LLM‑based routing, or capability‑based routing.

### Practical Architecture Blueprint
1. API / Gateway layer
2. Orchestrator service (task understanding, planning, agent & tool routing)
3. Specialist agent services (each with own prompt, policy, tools)
4. Shared services (memory, tool APIs, monitoring & guardrails)
5. Execution patterns (sequential, concurrent, handoff, group chat)
6. Failure handling (timeouts, retries, fallbacks)

## Query 2: AI agent MCP protocol tool orchestration
AI agents use the **Model Context Protocol (MCP)** as a standardized "USB‑C for tools" that lets an orchestrator agent discover tools, decide which to call, and sequence/chain them into workflows.

### What MCP Does in Tool Orchestration
- **Unified tool interface**: MCP defines a common schema for tools (inputs, outputs, parameter types, descriptions).
- **AI-first semantics ("skills")**: APIs, events, workflows packaged as agent skills/tools with semantic structure.
- **Bridge between AI and APIs/data**: MCP servers adapt local resources and remote services into MCP tools.
- **Governance boundary**: MCP defines what tools exist and with what semantics/permissions.

### Where Orchestration Lives vs. What MCP Provides
- **MCP protocol + servers**: Standardizes tool discovery, schemas, invocation. Makes tools "callable" and understandable by models.
- **Agent host / orchestrator**: Runs the LLM, interprets user intent, plans, sequences tool calls. Implements chaining, ordering, hand‑offs, retries.
- Key point: **MCP itself does not dictate execution order or workflows.** The orchestrator agent is responsible for orchestration.

### How Tool Use Works with MCP in an Agent Loop
1. **Initialization / discovery**: AI agent connects to MCP servers and requests available tools and schemas.
2. **Planning & decision**: LLM decides whether a tool is needed and which MCP tool matches the intent.
3. **Tool invocation**: Orchestrator calls the MCP tool with the arguments chosen by the model.
4. **Reasoning over results**: Orchestrator feeds the tool result back into the model.
5. **Chaining & multi‑step workflows**: LLM chains multiple MCP tools for complex requests.

### Patterns for Controlled Tool Orchestration with MCP
1. **Schema‑driven dependency hints**: MCP tools expose required inputs; LLM can discover tool dependencies.
2. **Server‑enforced sequencing via tokens**: Server generates validation tokens encoding allowed sequences.
3. **Orchestrator‑level workflows/recipes**: Platforms create recipes where APIs are orchestrated in pre-defined sequences.
4. **Multi‑agent orchestration via MCP**: MCP as communication layer between orchestrator and specialized agents/tools.

### MCP in Enterprise Orchestration Stacks
- **APIs** define what can be done.
- **MCP** defines how AI interacts with those capabilities.
- **Orchestration platform / agent framework** defines when and in what order things happen.

## Query 3: Cybersecurity in agentic systems with tool calling
Agentic cybersecurity systems with **tool calling** are vulnerable to prompt injection, excessive agency, tool poisoning, tool shadowing, and rugpull-style changes in tool behavior.

### Key Vulnerability Classes
- **Excessive agency**: Agent has more tools, permissions, or autonomy than needed.
- **Tool poisoning**: Malicious instructions embedded in a tool's description, schema, or examples.
- **Tool shadowing**: One tool's metadata influences how the agent uses another tool.
- **Rugpull attacks**: A tool or MCP server behaves safely at first, then later changes behavior.
- **Command execution abuse**: Coding agents with bash/run_code tools can be compromised if guardrails are weak.
- **Indirect prompt injection**: Malicious instructions hidden in emails, web pages, documents, API responses.

### MCP and Shared-Tool Architecture Risks
MCP and similar shared-tool architectures can concentrate risk: if many agents trust one server, a compromise or malicious metadata update can affect them broadly.

### Common Mitigations
- **Least privilege** for tools, permissions, and autonomy.
- **Human approval** for high-impact actions.
- **Strict parameter validation and schema enforcement**.
- **Signed tool manifests, version pinning, and tool audits**.
- **Logging and reasoning telemetry**.
- **MCP identity controls** such as mutual TLS and certificate pinning.
