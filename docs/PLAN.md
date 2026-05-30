# PLAN.md — Implementation Architecture Plan
## CrewAI LaTeX Book Publisher

**Version:** 1.0  
**Date:** 2026-05-30  
**Author:** Senior Software Architect (AI-Assisted)  
**Status:** Ready for TDD implementation  
**Derived from:** `docs/PRD.md`

---

## 1. Architecture Principles

Every decision in this plan is anchored to one of these four constraints from `CLAUDE.md`:

| Constraint | Architectural Response |
|------------|----------------------|
| 150-line cap | Each file has an explicit line budget; any approaching 120 lines is pre-split |
| TDD-first | Implementation order = test file → implementation file, no exceptions |
| No hardcoded hyperparameters | All constants flow from `Settings`; only security-invariant sets (import whitelists) live in code |
| No direct `client.messages.create()` | CrewAI's `Agent(llm=...)` is the single API abstraction; no raw Anthropic SDK calls in this project |

---

## 2. Complete Directory Tree

```
crewai-latex-publisher/
│
├── CLAUDE.md                          # behavioral contract (committed)
├── pyproject.toml                     # uv project manifest
├── .env                               # secrets — NEVER committed
├── .env.example                       # template with placeholder values
├── main.py                            # entry point: PublisherCrew().kickoff()
│
├── src/
│   ├── __init__.py                    # empty
│   ├── config.py                      # pydantic-settings Settings (~40 lines)
│   ├── crew.py                        # PublisherCrew + _load_skill() (~80 lines)
│   │
│   ├── agents/
│   │   ├── __init__.py                # empty
│   │   ├── outline_agent.py           # build_outline_agent() (~30 lines)
│   │   ├── content_agent.py           # build_content_agent() (~30 lines)
│   │   ├── bidi_agent.py              # build_bidi_agent() (~30 lines)
│   │   ├── figure_agent.py            # build_figure_agent() (~30 lines)
│   │   └── compiler_agent.py          # build_compiler_agent() (~30 lines)
│   │
│   ├── tasks/
│   │   ├── __init__.py                # empty
│   │   ├── outline_task.py            # build_outline_task() (~40 lines)
│   │   ├── content_task.py            # build_content_tasks() → list[Task] (~65 lines)
│   │   ├── bidi_task.py               # build_bidi_task() (~40 lines)
│   │   ├── figure_task.py             # build_figure_task() (~45 lines)
│   │   └── compile_task.py            # build_compile_task() (~45 lines)
│   │
│   └── tools/
│       ├── __init__.py                # empty
│       ├── latex_writer.py            # LatexWriterTool (~85 lines)
│       ├── python_runner.py           # PythonRunnerTool (~95 lines)
│       └── lualatex_runner.py         # LualatexRunnerTool + CompilationError (~90 lines)
│
├── skills/
│   ├── academic-outline/
│   │   └── SKILL.md                   # OutlineAgent backstory
│   ├── hebrew-academic-writing/
│   │   └── SKILL.md                   # ContentAgent backstory
│   ├── lualatex-bidi/
│   │   └── SKILL.md                   # BidiAgent backstory
│   ├── matplotlib-tikz/
│   │   └── SKILL.md                   # FigureAgent backstory
│   └── lualatex-build/
│       └── SKILL.md                   # CompilerAgent backstory
│
├── tests/
│   ├── conftest.py                    # shared pytest fixtures (~40 lines)
│   ├── test_config.py                 # Settings load + validation (~50 lines)
│   ├── test_latex_writer.py           # write/append/path-traversal tests (~80 lines)
│   ├── test_python_runner.py          # execution + import-whitelist tests (~90 lines)
│   ├── test_lualatex_runner.py        # log parsing + skipif lualatex absent (~70 lines)
│   ├── test_crew.py                   # skill injection + agent/task wiring (~80 lines)
│   └── test_integration.py            # end-to-end run marked @pytest.mark.slow (~60 lines)
│
├── docs/
│   ├── PRD.md
│   ├── PLAN.md                        ← this file
│   └── TODO.md
│
└── latex_output/                      # gitignored (except .gitkeep per subdirectory)
    ├── .gitkeep
    ├── assets/                        # attention_complexity.png
    │   └── .gitkeep
    ├── chapters/                      # ch1.tex … ch6.tex (generated)
    │   └── .gitkeep
    ├── figures/                       # sdp_attention.tex (TikZ snippet)
    │   └── .gitkeep
    ├── refs.bib                       # hand-authored; committed once
    └── main.tex                       # assembled by CompilerAgent (generated)
```

---

## 3. Module Breakdown and Line Budgets

### 3.1 `src/config.py` — Budget: 40 lines

**Responsibility:** Single source of truth for all tuneable values. Loaded once; shared via module-level `settings` singleton.

**Contents:**
- `class Settings(BaseSettings)` with 8 fields matching PRD §9
- `class Config` inner class: `env_file = ".env"`, `env_file_encoding = "utf-8"`
- Module-level `settings = Settings()` instantiation

**Key constraint:** No field may have a hardcoded literal that differs from `.env` — defaults here exist only for test environments where `.env` is absent. Production always overrides via `.env`.

**Sample skeleton:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LLM_MODEL: str = "claude-sonnet-4-6"
    ANTHROPIC_API_KEY: str
    MAX_AGENT_RETRIES: int = 3
    PYTHON_RUNNER_TIMEOUT_S: int = 60
    LUALATEX_BIN: str = "lualatex"
    OUTPUT_DIR: str = "latex_output"
    ASSETS_DIR: str = "latex_output/assets"
    MIN_PAGES: int = 15

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

---

### 3.2 `src/crew.py` — Budget: 80 lines

**Responsibility:** Owns the skill-loading contract, assembles agents and tasks via imported builders, exposes `PublisherCrew.kickoff()`.

**Contents:**
- `_load_skill(name: str) -> str` — the only place skill files are read
- `class PublisherCrew`
  - `__init__`: loads 5 skills, calls 5 agent builders, calls 5 task builders
  - `kickoff() -> str`: constructs `Crew(process=Process.sequential, ...)` and calls `.kickoff()`

**What `crew.py` must NOT contain:** Any LaTeX, Hebrew, or matplotlib knowledge. All domain content lives in `SKILL.md` files and task description strings.

**Why 80 lines is achievable:** Each agent/task is one function call imported from its own module. The crew only wires the graph.

---

### 3.3 Agent Modules (`src/agents/`) — Budget: 30 lines each

Each agent module exports exactly one factory function: `build_<name>_agent(backstory: str) -> Agent`.

**Pattern applied to all five agents:**
```python
from crewai import Agent
from src.config import settings
from src.tools.<tool> import <tool_instance>

def build_<name>_agent(backstory: str) -> Agent:
    return Agent(
        role="...",
        goal="...",
        backstory=backstory,   # injected by crew.py from SKILL.md
        tools=[...],
        llm=settings.LLM_MODEL,
        max_retry_limit=settings.MAX_AGENT_RETRIES,
        verbose=True,
    )
```

**Agent → Tool mapping:**

| Module | Agent Role | Tools |
|--------|-----------|-------|
| `outline_agent.py` | Academic Outline Architect | `latex_writer_tool` |
| `content_agent.py` | Hebrew Academic Writer | `latex_writer_tool` |
| `bidi_agent.py` | LaTeX BiDi Typesetting Specialist | `latex_writer_tool` |
| `figure_agent.py` | Scientific Figure Generator | `python_runner_tool`, `latex_writer_tool` |
| `compiler_agent.py` | LaTeX Build Engineer | `lualatex_runner_tool` |

**Line budget rationale:** With 7–8 lines of imports, a 20-line factory function, and no logic, each file safely sits at ~30 lines.

---

### 3.4 Task Modules (`src/tasks/`) — Budget: 40–65 lines each

Each module exports one factory function. Task descriptions embed all prompt engineering; agent modules remain description-free.

#### `outline_task.py` (~40 lines)
- `build_outline_task(agent) -> Task`
- Description instructs the agent to produce `latex_output/book_outline.json` with the exact 6-chapter schema from PRD §5.1
- `expected_output`: "Valid JSON file at `latex_output/book_outline.json`"

#### `content_task.py` (~65 lines)
- `build_content_tasks(agent, outline_task) -> list[Task]`
- Iterates `range(1, 7)`, building one `Task` per chapter
- Each task `context=[outline_task]` so it can read the outline
- Description is parameterized with chapter number, Hebrew title (from a module-level `CHAPTER_SPECS` list), and page budget
- `expected_output`: `"latex_output/chapters/ch{n}.tex file with no \\begin{{document}}`"

**`CHAPTER_SPECS` list** (6 tuples of `(ch_number, hebrew_title, page_count)`) is a code-level constant — it encodes fixed book structure, not a tuneable hyperparameter. This is consistent with CLAUDE.md §8 because the chapter titles and page counts are editorial choices, not configuration values.

#### `bidi_task.py` (~40 lines)
- `build_bidi_task(agent, content_tasks) -> Task`
- `context=content_tasks` (all 6) so agent can re-read chapter files
- Description mandates: validate and fix `ch1.tex`–`ch6.tex`; enforce Chapter 3 has ≥3 distinct BiDi constructs
- `expected_output`: "All six chapters updated in-place with no bidi warnings"

#### `figure_task.py` (~45 lines)
- `build_figure_task(agent, outline_task) -> Task`
- Description: write and execute a Python script to produce `assets/attention_complexity.png`; write TikZ block for scaled dot-product attention to `figures/sdp_attention.tex`
- Specifies the matplotlib script structure the agent must generate

#### `compile_task.py` (~45 lines)
- `build_compile_task(agent, bidi_task, figure_task) -> Task`
- `context=[bidi_task, figure_task]` so it can confirm artifacts exist
- Description: assemble `main.tex` preamble (exact packages from PRD §6.1) + 6 `\input{}` calls + `\printbibliography`; run `lualatex` twice
- `expected_output`: "`latex_output/main.pdf` exists, two-pass lualatex exits 0"

---

### 3.5 Tool Modules (`src/tools/`) — Budget: 85–95 lines each

#### `latex_writer.py` (~85 lines)

**Exports:** `latex_writer_tool` (a `BaseTool` instance)

**Internal structure:**
```
class LatexWriterInput(BaseModel):          # ~10 lines
    path: str
    content: str
    mode: Literal["write", "append"]

class LatexWriterTool(BaseTool):            # ~60 lines
    name = "latex_writer"
    description = "..."
    args_schema = LatexWriterInput

    def _validate_path(self, path: str) -> Path:   # path traversal guard
    def _run(self, path, content, mode) -> str:    # write/append logic

latex_writer_tool = LatexWriterTool()       # ~1 line
```

**Path traversal guard:** Resolves the path relative to `settings.OUTPUT_DIR`, then checks `resolved.is_relative_to(Path(settings.OUTPUT_DIR).resolve())`. Raises `ValueError` on violation.

---

#### `python_runner.py` (~95 lines)

**Exports:** `python_runner_tool`

**Internal structure:**
```
ALLOWED_IMPORTS: frozenset = frozenset({    # security invariant, not a hyperparameter
    "matplotlib", "numpy", "pathlib", "os"
})

class PythonRunnerInput(BaseModel):         # ~5 lines

class PythonRunnerTool(BaseTool):           # ~70 lines
    def _scan_imports(self, script: str) -> list[str]:
        # uses ast.parse() to extract all top-level import names
        # returns list of disallowed names

    def _run(self, script: str) -> str:
        # 1. call _scan_imports; raise ValueError if disallowed imports found
        # 2. write to tempfile
        # 3. subprocess.run(["python3", tmpfile], timeout=settings.PYTHON_RUNNER_TIMEOUT_S)
        # 4. return stdout or raise on non-zero returncode

python_runner_tool = PythonRunnerTool()
```

**Why `ALLOWED_IMPORTS` is not in `.env`:** It is a security constraint, not a tunable value. Changing it requires a code review, not a config change.

---

#### `lualatex_runner.py` (~90 lines)

**Exports:** `lualatex_runner_tool`, `CompilationError`

**Internal structure:**
```
class CompilationError(Exception): pass    # ~3 lines

class LualatexRunnerInput(BaseModel):      # ~8 lines
    tex_file: str
    passes: int = 2

class LualatexRunnerTool(BaseTool):        # ~65 lines
    def _build_cmd(self, tex_file: str) -> list[str]:
        # [settings.LUALATEX_BIN, "--interaction=nonstopmode",
        #  f"--output-directory={settings.OUTPUT_DIR}", tex_file]

    def _parse_log(self, log_path: Path) -> list[str]:
        # reads .log, greps for lines starting with "! LaTeX Error"
        # returns list of error lines

    def _run(self, tex_file, passes) -> dict:
        # runs _build_cmd N times
        # after final pass, calls _parse_log
        # raises CompilationError if errors found
        # returns {"success": True, "pdf_path": ..., "log_tail": ...}

lualatex_runner_tool = LualatexRunnerTool()
```

---

## 4. CrewAI Orchestration Flow

### 4.1 Process Mode

```python
Crew(
    agents=[outline_agent, content_agent, bidi_agent, figure_agent, compiler_agent],
    tasks=[outline_task, *content_tasks, figure_task, bidi_task, compile_task],
    process=Process.sequential,
    verbose=True,
)
```

`Process.sequential` guarantees tasks execute in list order. No parallelism — consistent with PRD §13 (parallelization explicitly deferred).

### 4.2 Task Execution Sequence

```
Step 1:  outline_task       → OutlineAgent
         Output: latex_output/book_outline.json

Step 2:  content_task[ch1]  → ContentAgent
         Input context: outline_task
         Output: latex_output/chapters/ch1.tex

Step 3:  content_task[ch2]  → ContentAgent
         Output: latex_output/chapters/ch2.tex

Step 4:  content_task[ch3]  → ContentAgent
         Output: latex_output/chapters/ch3.tex  ← BiDi showcase chapter

Step 5:  content_task[ch4]  → ContentAgent
         Output: latex_output/chapters/ch4.tex

Step 6:  content_task[ch5]  → ContentAgent
         Output: latex_output/chapters/ch5.tex

Step 7:  content_task[ch6]  → ContentAgent
         Output: latex_output/chapters/ch6.tex

Step 8:  figure_task        → FigureAgent
         Input context: outline_task
         Output: latex_output/assets/attention_complexity.png
                 latex_output/figures/sdp_attention.tex

Step 9:  bidi_task          → BidiAgent
         Input context: content_tasks[1..6]
         Output: latex_output/chapters/ch1-6.tex (validated, overwritten in-place)

Step 10: compile_task       → CompilerAgent
         Input context: bidi_task, figure_task
         Output: latex_output/main.tex (assembled)
                 latex_output/main.pdf (compiled, 2 passes)
```

### 4.3 Inter-Task Communication Contract

Agents communicate **exclusively through files on disk**. CrewAI `context=[...]` is used only to signal task ordering — the actual data is always read from `latex_output/` by the receiving agent's tool or by the LLM reading the task description.

This means every intermediate artifact is independently inspectable and re-runnable without re-executing upstream tasks. This is the critical debugging affordance for a 15-page book generation pipeline.

### 4.4 Chapter 3 BiDi Showcase Guarantee

`bidi_task` description must explicitly state:

> "For `ch3.tex` specifically, verify and enforce that it contains at minimum three distinct BiDi constructs: (1) an RTL paragraph with inline `\textenglish{}` terms, (2) an LTR `equation` environment, (3) a `\begin{LTR}...\end{LTR}` block. If any are missing, add them."

This elevates the BiDi showcase requirement from a passive check to an active enforcement mandate.

---

## 5. Skills Injection Mechanism

### 5.1 The Loading Contract (implemented in `src/crew.py`)

```python
from pathlib import Path

def _load_skill(name: str) -> str:
    """Read SKILL.md for the named skill directory."""
    path = Path("skills") / name / "SKILL.md"
    return path.read_text(encoding="utf-8")
```

This is the **only** place in the codebase where a `SKILL.md` file is read. Tests will mock or stub this function.

### 5.2 Injection Point in `PublisherCrew.__init__`

```python
class PublisherCrew:
    def __init__(self):
        # Skills loaded first — fail fast if any SKILL.md is missing
        outline_skill   = _load_skill("academic-outline")
        content_skill   = _load_skill("hebrew-academic-writing")
        bidi_skill      = _load_skill("lualatex-bidi")
        figure_skill    = _load_skill("matplotlib-tikz")
        compiler_skill  = _load_skill("lualatex-build")

        # Agents constructed with skills as backstory
        self.outline_agent  = build_outline_agent(outline_skill)
        self.content_agent  = build_content_agent(content_skill)
        self.bidi_agent     = build_bidi_agent(bidi_skill)
        self.figure_agent   = build_figure_agent(figure_skill)
        self.compiler_agent = build_compiler_agent(compiler_skill)

        # Tasks wired to agents
        self.outline_task   = build_outline_task(self.outline_agent)
        self.content_tasks  = build_content_tasks(self.content_agent, self.outline_task)
        self.figure_task    = build_figure_task(self.figure_agent, self.outline_task)
        self.bidi_task      = build_bidi_task(self.bidi_agent, self.content_tasks)
        self.compile_task   = build_compile_task(self.compiler_agent,
                                                 self.bidi_task, self.figure_task)
```

### 5.3 What Each `SKILL.md` Must Contain

| Skill File | Required Content |
|-----------|-----------------|
| `academic-outline/SKILL.md` | JSON schema for `book_outline.json`; chapter planning conventions; academic citation norms |
| `hebrew-academic-writing/SKILL.md` | Hebrew academic register; RTL paragraph structure; `\textenglish{}` macro usage; when NOT to translate a term |
| `lualatex-bidi/SKILL.md` | LuaLaTeX `bidi` package rules; `polyglossia` language switching; common RTL/LTR pitfalls; validation checklist |
| `matplotlib-tikz/SKILL.md` | matplotlib save-as-PNG at 300 dpi; axis labeling; TikZ syntax for formula diagrams; integration with `\includegraphics` |
| `lualatex-build/SKILL.md` | `lualatex` CLI flags; two-pass strategy; log parsing heuristics; preamble assembly rules; `\input{}` ordering |

### 5.4 Enforcement: No Inline Domain Knowledge in `.py` Files

A code reviewer must be able to grep for any LaTeX package name, Hebrew word, or matplotlib function in all `.py` files and find **zero matches** outside of test fixtures. All such content belongs in `SKILL.md` files or task description strings in `tasks/`.

---

## 6. Dependency Graph

```
main.py
  └── src/crew.py
        ├── src/config.py                    (settings singleton)
        ├── src/agents/outline_agent.py
        │     └── src/tools/latex_writer.py
        ├── src/agents/content_agent.py
        │     └── src/tools/latex_writer.py
        ├── src/agents/bidi_agent.py
        │     └── src/tools/latex_writer.py
        ├── src/agents/figure_agent.py
        │     ├── src/tools/python_runner.py
        │     └── src/tools/latex_writer.py
        ├── src/agents/compiler_agent.py
        │     └── src/tools/lualatex_runner.py
        ├── src/tasks/outline_task.py
        ├── src/tasks/content_task.py        (imports CHAPTER_SPECS constant)
        ├── src/tasks/bidi_task.py
        ├── src/tasks/figure_task.py
        └── src/tasks/compile_task.py
```

**No circular imports.** Tools do not import from agents or tasks. Tasks do not import from agents. Agents do not import from tasks. `config.py` is imported by everything but imports nothing from `src/`.

---

## 7. Test Plan

### `tests/conftest.py` (~40 lines)
- `tmp_output_dir` fixture: creates a temporary directory, patches `settings.OUTPUT_DIR` and `settings.ASSETS_DIR`
- `mock_settings` fixture: `Settings` instance with test values, no `.env` required

### `tests/test_config.py` (~50 lines)
- `test_settings_load_from_env`: monkeypatch env vars, verify `settings.LLM_MODEL` etc.
- `test_missing_api_key_raises`: verify `Settings()` raises without `ANTHROPIC_API_KEY`
- `test_defaults_applied`: verify default values match PRD §9

### `tests/test_latex_writer.py` (~80 lines)
- `test_write_creates_file`: write mode creates a new file with correct content
- `test_append_adds_content`: append mode adds to existing file
- `test_path_traversal_rejected`: `../../../etc/passwd` raises `ValueError`
- `test_creates_parent_directories`: deeply nested path is created automatically
- `test_utf8_encoding`: Hebrew content round-trips correctly

### `tests/test_python_runner.py` (~90 lines)
- `test_valid_script_executes`: simple matplotlib script produces a PNG
- `test_disallowed_import_rejected`: `import subprocess` raises `ValueError` before execution
- `test_timeout_enforced`: script with `time.sleep(9999)` raises `TimeoutExpired`
- `test_syntax_error_reported`: malformed Python returns stderr in result
- `test_ast_scan_catches_from_import`: `from os import system` is caught

### `tests/test_lualatex_runner.py` (~70 lines)
- `@pytest.mark.skipif(shutil.which("lualatex") is None, reason="lualatex not installed")`
- `test_log_parser_detects_error`: feed a log string with `! LaTeX Error`, verify `CompilationError`
- `test_log_parser_clean`: clean log returns empty error list
- `test_command_built_correctly`: verify `_build_cmd` output matches expected argv
- Integration test (skipped if no binary): minimal `.tex` compiles successfully

### `tests/test_crew.py` (~80 lines)
- `test_load_skill_reads_file`: write a temp `SKILL.md`, verify `_load_skill()` returns its content
- `test_load_skill_missing_raises`: `FileNotFoundError` when skill file absent
- `test_all_skills_injected_as_backstory`: mock all `SKILL.md` files; construct `PublisherCrew`; assert each agent's `backstory` equals the mocked content
- `test_task_count`: verify crew has exactly 10 tasks (1 outline + 6 content + 1 figure + 1 bidi + 1 compile)
- `test_no_hardcoded_backstory`: assert no agent backstory string contains "LaTeX" or "Hebrew" (proving skills are loaded, not inline)

### `tests/test_integration.py` (~60 lines)
- `@pytest.mark.slow` — excluded from default `pytest` run; included via `pytest -m slow`
- `test_full_pipeline_produces_pdf`: run `PublisherCrew().kickoff()`; assert `latex_output/main.pdf` exists; assert `pdfinfo` reports ≥15 pages
- Requires: `ANTHROPIC_API_KEY` in env, `lualatex` installed, Hebrew font available

---

## 8. Implementation Sequence (TDD Order)

The following order guarantees each step has a failing test before code is written and that no module is implemented before its dependencies are ready.

| Step | Write Test First | Then Implement | Gate Before Next |
|------|-----------------|----------------|-----------------|
| 1 | `tests/test_config.py` | `src/config.py` | `pytest tests/test_config.py` exits 0 |
| 2 | `tests/test_latex_writer.py` | `src/tools/latex_writer.py` | `pytest tests/test_latex_writer.py` exits 0 |
| 3 | `tests/test_python_runner.py` | `src/tools/python_runner.py` | `pytest tests/test_python_runner.py` exits 0 |
| 4 | `tests/test_lualatex_runner.py` | `src/tools/lualatex_runner.py` | `pytest tests/test_lualatex_runner.py` exits 0 |
| 5 | — | All 5 `SKILL.md` files authored | Files present, non-empty |
| 6 | `tests/test_crew.py` | All 5 agent modules + `src/crew.py` | `pytest tests/test_crew.py` exits 0 |
| 7 | (covered by test_crew.py) | All 5 task modules | `pytest tests/test_crew.py -v` exits 0 |
| 8 | — | `latex_output/refs.bib` (6 entries) | File present, valid BibTeX |
| 9 | `tests/test_integration.py` | `main.py` wired to `PublisherCrew().kickoff()` | `pytest -m slow` exits 0 |

After every step:
```bash
uv run ruff check .
uv run pytest --cov=src --cov-fail-under=80
wc -l src/**/*.py   # no file may exceed 150 lines
```

---

## 9. Line Budget Summary

| File | Estimated Lines | Headroom to 150 |
|------|----------------|-----------------|
| `src/config.py` | 40 | 110 |
| `src/crew.py` | 80 | 70 |
| `src/agents/outline_agent.py` | 30 | 120 |
| `src/agents/content_agent.py` | 30 | 120 |
| `src/agents/bidi_agent.py` | 30 | 120 |
| `src/agents/figure_agent.py` | 30 | 120 |
| `src/agents/compiler_agent.py` | 30 | 120 |
| `src/tasks/outline_task.py` | 40 | 110 |
| `src/tasks/content_task.py` | 65 | 85 |
| `src/tasks/bidi_task.py` | 40 | 110 |
| `src/tasks/figure_task.py` | 45 | 105 |
| `src/tasks/compile_task.py` | 45 | 105 |
| `src/tools/latex_writer.py` | 85 | 65 |
| `src/tools/python_runner.py` | 95 | 55 |
| `src/tools/lualatex_runner.py` | 90 | 60 |

**Highest-risk files** for approaching the limit: `python_runner.py` and `lualatex_runner.py`. If either exceeds 120 lines during implementation, extract helpers immediately:
- `python_runner.py` → split `_import_scanner.py` if needed
- `lualatex_runner.py` → split `_log_parser.py` if needed

---

## 10. Risk Checkpoints

| Risk | Detection Point | Response |
|------|----------------|----------|
| Agent produces syntactically invalid LaTeX | BidiAgent task execution | BidiAgent's description explicitly asks it to fix fragments; `lualatex_runner` raises `CompilationError` with log tail |
| Hebrew font unavailable on build host | `compile_task` execution | Preamble uses `fontspec` fallback chain: `David CLM` → `Frank Ruehl CLM` → `Noto Serif Hebrew` |
| `python_runner` generates a broken matplotlib script | `figure_task` execution | `PythonRunnerTool._run` returns stderr; FigureAgent retries up to `MAX_AGENT_RETRIES` |
| `content_task.py` grows past 120 lines | During implementation step 7 | Extract `CHAPTER_SPECS` into a sibling `_chapter_specs.py` (~15 lines) |
| `crew.py` wiring grows past 120 lines | During implementation step 6 | Extract `_build_all_agents()` and `_build_all_tasks()` into private helpers; still within one file |
| lualatex absent in CI | `test_lualatex_runner.py` | `@pytest.mark.skipif(shutil.which("lualatex") is None, ...)` skips binary-dependent tests |
