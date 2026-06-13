# CLAUDE.md — Behavioral Contract for AI-Assisted Development

This file governs how Claude (and any AI assistant) must behave when working in this repository. All rules below are enforced during every session. Non-compliance invalidates the architectural guarantees described in `docs/PRD.md`.

---

## Part I: Karpathy's 4 Core Rules

### 1. Think Before Coding
Before writing or modifying any code, state the problem, identify the affected modules, and verify there is a failing test that justifies the change. Never start an implementation without first understanding why it is needed.

### 2. Simplicity First
Prefer the simplest solution that satisfies the failing test. Do not introduce abstractions, generics, or helper utilities that are not immediately required. Three similar lines are better than a premature abstraction.

### 3. Surgical Changes
Edits must be minimal and targeted. Do not refactor surrounding code while fixing a bug. Do not rename symbols, reorganize imports, or clean up unrelated logic in the same commit as a functional change.

### 4. Goal-Driven Execution
Every action must trace back to a specific task in `docs/TODO.md` or an explicit user instruction. Do not add features, logging, or error handling for hypothetical future scenarios that are not part of the current goal.

---

## Part II: Project-Specific Constraints

### 5. All LLM Calls Must Route Through CrewAI Agent Framework
No module may instantiate `anthropic.Anthropic()` and call `.messages.create()` directly. Every LLM call must go through a CrewAI `Agent` whose `llm=` parameter is set from `src/config.py` via `make_llm()`, `make_llm_fast()`, or `make_llm_smart()`. This enforces centralized model selection, rate-limit handling, and the circuit-breaker retry policy defined in `MAX_AGENT_RETRIES`.

**Violation pattern to avoid:**
```python
# FORBIDDEN — direct SDK call
client = anthropic.Anthropic()
response = client.messages.create(model=..., messages=...)
```

**Required pattern:**
```python
# CORRECT — LLM configured via settings, passed to CrewAI Agent
from src.config import make_llm
agent = Agent(role=..., llm=make_llm(), ...)
```

### 6. Hard 150-Line Limit Per File
No Python source file in `src/` may exceed 150 lines. If an implementation requires more, it must be split into focused submodules. Verify with `wc -l <file>` before committing. This limit enforces single-responsibility and keeps the codebase auditable.

### 7. Strict TDD-First Mandate
No implementation code may be written before a failing test exists for it. The workflow is always:

1. Write a test in `tests/` that fails (`pytest` exits non-zero).
2. Write the minimum implementation to make the test pass.
3. Refactor only under green.

Committing implementation code without a corresponding test is a contract violation.

### 8. No Hardcoded Hyperparameters in Python Files
All tuneable values (token budgets, iteration limits, model IDs, binary paths, output directories) must be sourced from `.env` via `src/config.py` (pydantic-settings `Settings` class). Embedding a magic number directly in a `.py` file is forbidden.

**Violation pattern to avoid:**
```python
# FORBIDDEN — hardcoded hyperparameter
MAX_ITER = 15
LUALATEX_BIN = "lualatex"
```

**Required pattern:**
```python
# CORRECT — loaded from settings
from src.config import settings
max_iter = settings.MAX_ITER
lualatex_bin = settings.LUALATEX_BIN
```

### 9. One-Artifact-Per-Task Scope
Each CrewAI task must produce exactly one discrete output artifact (one chapter `.tex` file, one `book_outline.json`, one compiled `main.pdf`). If a downstream agent needs a prior artifact, it reads from `latex_output/` on disk — it must not reconstruct it from context. This keeps per-task context growth bounded and makes every pipeline step independently re-runnable from its checkpoint file.

---

## Enforcement

Before any commit:
```bash
uv run ruff check .          # must exit 0
uv run pytest --cov=src      # must exit 0, coverage must not decrease
wc -l src/**/*.py            # no file may exceed 150 lines
```

These gates are also enforced by GitHub Actions CI on every push.

---

## Part III: Production Robustness Rules

### 10. Chunked Writing Strategy — 25-30 Lines Maximum Per Call
**NEVER attempt to write an entire chapter or large text block in a single tool call.** Long strings cause JSON truncation (`Unterminated string` error) which silently drops `content` and `mode`, producing a Pydantic validation error.

**Hard limit: each `content` argument must be at most 25-30 lines.** Always build large files iteratively:
- First chunk: `mode="write"` to create the file (≤ 30 lines).
- Every subsequent chunk: `mode="append"` (≤ 30 lines each).
- Each tool call must explicitly include all three arguments: `path`, `content`, `mode`.

### 11. Hard Circuit Breaker — Three Strikes, Then Halt
If any tool or compilation step fails **three consecutive times**, stop immediately and report the failure explicitly. Do not enter an infinite retry loop. The `MAX_AGENT_RETRIES` setting enforces this at the agent level; tasks must not manually retry beyond it.

**Violation pattern to avoid:**
```
# FORBIDDEN — silent infinite loop
while True:
    try: tool_call()
    except: continue
```

### 12. Mandatory Checkpoints in Multi-Step Tasks
After completing each discrete step in a multi-step task, the agent must emit a one-line checkpoint: what was completed and what remains. This prevents silent partial completion being reported as success.

Example format: `[CHECKPOINT] Step 1 done: ch3.md written (847 words). Remaining: convert to .tex.`

### 13. Explicit Failure — Never Report Success for a Skipped Step
If a tool call fails, a file was not written, or a compilation produced errors, the agent must report the exact failure. Reporting "task complete" when the output file does not exist is a contract violation. Expose uncertainty by default: if unsure whether a step succeeded, say so.
