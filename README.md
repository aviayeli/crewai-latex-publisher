# crewai-latex-publisher

A multi-agent CrewAI pipeline that researches, writes, and compiles a
typeset Hebrew-English bilingual academic book on Transformer models — fully
automated from Perplexity research to a 15-page LuaLaTeX PDF.

---

## Architecture

```
Perplexity Research → Outline Planning → Markdown Generation (×6 chapters)
    → Pandoc Conversion → BiDi Validation → LuaLaTeX + Biber Compilation
```

Seven specialised agents collaborate via a hierarchical CrewAI process. Each
agent is injected with a domain-specific skill file from `skills/`. See
[`docs/PRD_latex_pipeline.md`](docs/PRD_latex_pipeline.md) for the complete
mechanism reference.

---

## Quick Start

```bash
cp .env.example .env       # add ANTHROPIC_API_KEY and PERPLEXITY_API_KEY
uv sync
uv run python main.py      # runs the full pipeline
```

Output PDF: `latex_output/main.pdf`

---

## Human-in-the-Loop (HITL) Gate

Before the 4-step LuaLaTeX + Biber compilation executes, the pipeline can
pause and require explicit operator approval. This gives a human the chance to
inspect the generated `.tex` files before committing compute to compilation.

**Enable the gate:**

```bash
# .env
HITL_ENABLED=true
```

When enabled, the terminal will display:

```
[HITL] Press Y to execute the 4-step PDF compilation for 'latex_output/main.tex' [Y/n]:
```

- Enter **Y** to proceed with compilation.
- Enter anything else to abort with a clear error message.

**Disabled by default** so automated CI runs and tests are unaffected.
The gate is implemented in `src/tools/lualatex_runner.py` and fully tested
in `tests/test_lualatex_runner.py`.

---

## LaTeX Pipeline — Mechanism Reference

Full documentation of every conversion step is in
[`docs/PRD_latex_pipeline.md`](docs/PRD_latex_pipeline.md), including:

- Pandoc CLI flags and `markdown+raw_tex` passthrough rationale
- Two-pattern `\textenglish{}` regex unescaping protocol
- 4-step LuaLaTeX / Biber compilation sequence
- Font stack: David CLM (Hebrew) · Courier New · Arial
- All `settings` fields and their defaults

---

## Cost Optimisation — 75% Token Cost Reduction

The pipeline was migrated from `claude-sonnet-4-6` to `claude-haiku-4-5`
without any quality regression on Hebrew academic text generation.

![Cost comparison bar chart: Sonnet 4.6 vs Haiku 4.5](assets/cost_optimization.png)

**Estimated per-run savings:**

| Model | Input $/MTok | Output $/MTok | Est. cost / run |
|---|---|---|---|
| claude-sonnet-4-6 (previous) | $3.00 | $15.00 | ~$1.56 |
| claude-haiku-4-5 (current)   | $0.80 | $4.00  | ~$0.42 |

> ~75% reduction in token spend with equivalent output quality for
> structured Hebrew academic text.

Model is configurable via `LLM_MODEL=` in `.env` — never hardcoded.

---

## Skills Inventory

| Skill file | Agent | Purpose |
|---|---|---|
| `skills/manager/SKILL.md` | ManagerAgent | Hierarchical orchestration |
| `skills/perplexity-research/SKILL.md` | ResearcherAgent | Perplexity API search |
| `skills/academic-outline/SKILL.md` | OutlineAgent | 6-chapter JSON outline |
| `skills/hebrew-academic-writing/SKILL.md` | ContentAgent | Hebrew prose writing |
| `skills/lualatex-bidi/SKILL.md` | BidiAgent | BiDi validation (10-item checklist) |
| `skills/matplotlib-tikz/SKILL.md` | FigureAgent | Chart and TikZ generation |
| `skills/lualatex-build/SKILL.md` | CompilerAgent | Pandoc → LuaLaTeX pipeline |
| `skills/latex_expert/SKILL.md` | CompilerAgent | Font injection + regex unescaping |

---

## Configuration

All tuneable values are set in `.env` (see `.env.example`). Key fields:

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Required |
| `PERPLEXITY_API_KEY` | — | Required |
| `LLM_MODEL` | `anthropic/claude-haiku-4-5-20251001` | Model for all agents |
| `MAX_AGENT_RETRIES` | `3` | Circuit breaker (3 strikes → halt) |
| `HITL_ENABLED` | `false` | Enable operator approval gate |
| `OUTPUT_DIR` | `latex_output` | Output directory |

---

## Enterprise Grade & Security

### Red-Team Attack Coverage

`tests/red_team_attack.py` simulates two adversarial attack classes against
the tool layer and asserts each is safely blocked:

| Attack class | Attack vector | Defence layer | Result |
|---|---|---|---|
| **Prompt Injection** | Path traversal (`../../etc/passwd`) | `MarkdownConverterTool._validate_path()` | `ValueError: escapes` |
| **Prompt Injection** | Absolute path injection (`/etc/shadow`) | `_validate_path()` | `ValueError: escapes` |
| **Prompt Injection** | Null-byte injection (`file\x00.md`) | Python `Path` constructor | `ValueError` |
| **Tool Misuse** | `import subprocess` in script | `PythonRunnerTool._scan_imports()` AST scan | Flagged + blocked |
| **Tool Misuse** | `import sys; sys.exit()` | AST scan | Flagged + blocked |
| **Tool Misuse** | `from subprocess import run` | AST scan (from-import form) | Flagged + blocked |
| **Tool Misuse** | Chained `import socket, subprocess, ctypes` | AST scan | All 3 flagged |

```bash
uv run pytest tests/red_team_attack.py -v   # 18 tests, all pass
```

**Known limitation** (documented, not fixed): `exec("import subprocess")` bypasses
the static AST scan. A full sandbox (seccomp, gVisor) is required to block
dynamic eval attacks at the OS level.

---

### CI/CD Pipeline

Every push and pull request triggers `.github/workflows/ci.yml`, which enforces:

| Gate | Command | Requirement |
|---|---|---|
| Zero lint violations | `ruff check .` | exit 0 |
| Coverage threshold | `pytest --cov=src --cov-fail-under=85` | ≥ 85% |
| 150-line budget | `find src -name "*.py" \| xargs wc -l` | no file > 150 lines |

---

### MCP (Model Context Protocol) Server

`src/tools/mcp_latex_server.py` exposes the Markdown→LaTeX converter as a
JSON-RPC 2.0 MCP endpoint, enabling horizontal agent interoperability with any
MCP-compatible orchestrator (Claude Desktop, OpenAI Agents SDK, LangGraph, etc.).

**Supported methods:**

| JSON-RPC method | Description |
|---|---|
| `tools/list` | Returns the tool manifest (name, description, input schema) |
| `tools/call` | Dispatches to `markdown_converter_tool` with path-safety validation |

**Usage example:**

```python
from src.tools.mcp_latex_server import mcp_latex_server

# Discover available tools
resp = mcp_latex_server.handle({"jsonrpc": "2.0", "method": "tools/list", "id": 1})
# → {"jsonrpc": "2.0", "result": {"tools": [{"name": "markdown_to_latex", ...}]}, "id": 1}

# Call the converter
resp = mcp_latex_server.handle({
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {"name": "markdown_to_latex",
               "arguments": {"md_path": "chapters/ch1.md", "tex_path": "chapters/ch1.tex"}},
    "id": 2,
})
```

Path-traversal attacks routed through the MCP endpoint are still blocked by
`_validate_path()` and returned as JSON-RPC `-32602` errors.

---

### OAT Parameter Analysis Notebook

`notebooks/parameter_analysis.ipynb` performs a One-at-a-Time (OAT) sensitivity
analysis on two key pipeline knobs:

- **`MAX_TOKENS`** (512 → 8 192): cost scales linearly; completion rate saturates
  at 4 096 — the current default is at the knee of the curve.
- **`chunk_size`** (300 → 3 000 chars): write operations drop with larger chunks
  but JSON truncation risk follows a logistic curve that inflects at ~900 chars —
  exactly the CLAUDE.md §10 hard limit.

The combined heatmap (cost × risk) confirms the current defaults occupy the
optimal low-cost / low-risk quadrant.

```bash
jupyter lab notebooks/parameter_analysis.ipynb
```

---

## Testing

```bash
uv run ruff check .                          # lint — must exit 0
uv run pytest --cov=src --cov-fail-under=85  # ≥ 85% coverage
uv run pytest tests/red_team_attack.py -v    # security gate
wc -l src/**/*.py                            # no src/ file may exceed 150 lines
```

CI enforces all three gates on every push via `.github/workflows/ci.yml`.

---

## Generating the Cost Chart

```bash
uv run python scripts/generate_cost_chart.py
# → assets/cost_optimization.png
```
