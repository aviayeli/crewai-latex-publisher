# PRD — HW3: CrewAI LaTeX Book Publisher
## ארכיטקטורת ה-Transformer: ממודלים קלאסיים ועד למודלי שפה גדולים

**Version:** 1.0  
**Date:** 2026-05-30  
**Owner:** Avi Ayeli  
**Status:** Approved — implementation begins after this document is committed.

---

## 1. Problem Statement

We need a fully automated multi-agent pipeline that produces a **compilable, 15-page academic book** in Hebrew/English about the Transformer architecture. The book must be typeset in LuaLaTeX (to support right-to-left Hebrew), include all required academic elements (TOC, tables, figures, math, bibliography), and emerge from a CrewAI agent crew — no human author writes a single line of LaTeX manually.

The core challenge is **coordination**: content agents, formatting agents, and a figure-generation agent must each produce output that is composable into one coherent `.tex` project without merge conflicts or encoding errors.

---

## 2. Goals

| # | Goal | Measure of Success |
|---|------|--------------------|
| G1 | Compilable LaTeX output | `lualatex main.tex` exits 0 with no errors; 4-step pipeline (lualatex → biber → lualatex → log parse) resolves TOC, citations, and cross-references |
| G2 | Hebrew academic prose | At least 13 of 15 pages contain Hebrew body text |
| G3 | Valid BiDi mixing | At least one full chapter mixes Hebrew paragraphs with inline English terms, code identifiers, and formulas without bidi warnings |
| G4 | All required LaTeX elements | Cover, Headers/Footers, TOC, ≥1 Table, ≥1 Image, ≥1 Math formula, ≥1 Python-generated graph, BibTeX bibliography |
| G5 | Skills pattern enforced | Every agent's LaTeX/BiDi expertise is injected via a `SKILL.md` file, not baked into the agent backstory string |
| G6 | All CLAUDE.md constraints satisfied | 150-line cap, TDD, no hardcoded hyperparameters, all API calls via `ApiGatekeeper` |

## 3. Non-Goals

- Interactive UI or web frontend.
- Support for compilers other than LuaLaTeX (no pdflatex, no XeLaTeX fallback).
- Multi-language books beyond Hebrew + English.
- More than one run mode (no CLI flags, no config selection at runtime beyond `.env`).
- Automatic grammar or style correction of generated Hebrew prose.

---

## 4. System Architecture

```
main.py
  └── PublisherCrew (src/crew.py)  — hierarchical process, manager_agent orchestrates
        ├── agents/
        │     ├── manager_agent.py      — Project Manager; orchestrates all workers
        │     ├── researcher_agent.py   — Perplexity research; produces raw research notes
        │     ├── outline_agent.py      — plans chapter structure from research
        │     ├── content_agent.py      — writes Hebrew prose per chapter
        │     ├── bidi_agent.py         — enforces BiDi correctness in LaTeX
        │     ├── figure_agent.py       — generates Python graph + TikZ math figure
        │     └── compiler_agent.py     — assembles final .tex, runs lualatex
        ├── tasks/
        │     ├── research_task.py
        │     ├── outline_task.py
        │     ├── content_task.py
        │     ├── bidi_task.py
        │     ├── figure_task.py
        │     ├── figure_embed_task.py
        │     └── compile_task.py
        ├── tools/
        │     ├── latex_writer.py        — writes/appends .tex fragment files
        │     ├── python_runner.py       — executes graph-generation scripts in sandbox
        │     ├── markdown_converter.py  — pandoc Markdown → LaTeX fragment conversion
        │     └── lualatex_runner.py     — shells out to lualatex, captures log
        └── config.py                   — pydantic-settings Settings, reads from .env
```

### 4.1 Data Flow

```
research_task  →  [raw/research_raw.md]
                         │
                   outline_task  →  [book_outline.json]
                         │
              ┌──────────┴──────────┐
         content_task           figure_task
              │                      │
   [chapters/*.md → *.tex]    [assets/graph.png]
              │                      │
              └──────────┬──────────┘
                    bidi_task
                         │
              [chapters/*.tex  (bidi-validated)]
                         │
                figure_embed_task
                         │
                   compile_task
                         │
              [latex_output/main.pdf]
```

All intermediate artifacts are plain files under `latex_output/`. Agents communicate **only through files** — no in-memory object passing between CrewAI tasks. This makes every step independently debuggable and re-runnable.

---

## 5. Agent Definitions

Each agent must load its domain expertise from the corresponding `SKILL.md` file. The skill content is injected as the agent's `backstory` at crew construction time (see §7).

The pipeline uses **7 agents** under a hierarchical CrewAI process: one manager agent that delegates, and six worker agents.

### 5.0 ManagerAgent

| Field | Value |
|-------|-------|
| **Role** | Project Manager |
| **Goal** | Orchestrate the full pipeline: delegate research → outline → content → bidi → figure → compile in the correct dependency order; escalate if any worker trips the circuit breaker |
| **Skill** | `skills/manager/SKILL.md` |
| **Tools** | None (manager agent; delegation only) |
| **Output** | Coordination only — no file artifacts |

The ManagerAgent uses the CrewAI `hierarchical` process mode. All other agents are workers that receive delegated tasks from the manager.

### 5.1 ResearcherAgent

| Field | Value |
|-------|-------|
| **Role** | Academic Researcher |
| **Goal** | Query Perplexity for academic sources on the article topic; write a structured research-notes Markdown file that downstream agents use to ground the generated content |
| **Skill** | `skills/perplexity-research/SKILL.md` |
| **Tools** | `perplexity_search`, `latex_writer` |
| **Output** | `latex_output/raw/research_raw.md` |

### 5.2 OutlineAgent

| Field | Value |
|-------|-------|
| **Role** | Academic Outline Architect |
| **Goal** | Produce a JSON outline with exactly 6 chapters, each with a title (Hebrew), estimated page count, and list of key concepts |
| **Skill** | `skills/academic-outline/SKILL.md` |
| **Tools** | `latex_writer` (to persist outline) |
| **Output** | `latex_output/book_outline.json` |

**Chapter structure (fixed):**

| Ch | Hebrew Title | Content Focus | Target Pages |
|----|-------------|----------------|--------------|
| 1 | מבוא: גבולות מודלי ה-RNN | RNN bottleneck, motivation | 2 |
| 2 | מנגנון תשומת הלב (Attention) | Bahdanau, scaled dot-product | 3 |
| 3 | ארכיטקטורת ה-Transformer המקורית | Vaswani et al. 2017, encoder-decoder | 3 |
| 4 | מודלים מבוססי Transformer: BERT ו-GPT | Pre-training paradigms | 2.5 |
| 5 | מודלי שפה גדולים (LLMs) | GPT-3/4, scaling laws, emergent abilities | 2.5 |
| 6 | סיכום ומבט לעתיד | Open problems, future directions | 2 |

### 5.3 ContentAgent

| Field | Value |
|-------|-------|
| **Role** | Hebrew Academic Writer |
| **Goal** | Write fluent Hebrew academic prose for each chapter, embedding English technical terms inline using the `\textenglish{}` macro |
| **Skill** | `skills/hebrew-academic-writing/SKILL.md` |
| **Tools** | `latex_writer` |
| **Output** | `latex_output/chapters/ch{1-6}.tex` (one fragment per chapter) |

The agent receives one chapter spec at a time from `book_outline.json` and writes its `.tex` fragment. It must not include `\begin{document}` — fragments are assembled by the compiler agent.

### 5.4 BidiAgent

| Field | Value |
|-------|-------|
| **Role** | LaTeX BiDi Typesetting Specialist |
| **Goal** | Validate and fix every chapter `.tex` fragment for LuaLaTeX bidi compliance: correct use of `\textdir`, `\textenglish{}`, `\begin{LTR}`, formula wrapping, and no raw ASCII inside RTL paragraphs |
| **Skill** | `skills/lualatex-bidi/SKILL.md` |
| **Tools** | `latex_writer` (overwrites fragments in place) |
| **Output** | Updated `latex_output/chapters/ch{1-6}.tex` |

Chapter 3 is designated the **primary BiDi showcase chapter**. The `bidi_task` must verify it contains at least 3 distinct BiDi constructs (mixed paragraph, inline English, LTR math block).

### 5.5 FigureAgent

| Field | Value |
|-------|-------|
| **Role** | Scientific Figure Generator |
| **Goal** | (a) Write and execute a Python script that produces `assets/attention_complexity.png` — a matplotlib graph comparing the O(n²) complexity of self-attention vs. O(n) of RNN per layer; (b) write a standalone TikZ snippet for the Scaled Dot-Product Attention formula block |
| **Skill** | `skills/matplotlib-tikz/SKILL.md` |
| **Tools** | `python_runner`, `latex_writer` |
| **Output** | `latex_output/assets/attention_complexity.png`, `latex_output/figures/sdp_attention.tex` |

The math formula that must appear in the book:

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V$$

This must be typeset in LaTeX as a numbered `equation` environment.

### 5.6 CompilerAgent

| Field | Value |
|-------|-------|
| **Role** | LaTeX Build Engineer |
| **Goal** | Assemble all fragments into `latex_output/main.tex`, run the 4-step LuaLaTeX + Biber pipeline (lualatex → biber → lualatex → log parse), and confirm `main.pdf` is produced with no errors |
| **Skill** | `skills/lualatex-build/SKILL.md` |
| **Tools** | `lualatex_runner` |
| **Output** | `latex_output/main.pdf` |

The compiler agent owns the **preamble** (see §6.1). It must not modify chapter content — it only assembles via `\input{}` directives.

---

## 6. LaTeX Project Specification

### 6.1 Preamble Requirements

The `main.tex` preamble must include at minimum:

```latex
\documentclass[12pt, a4paper]{book}
\usepackage{polyglossia}
\setmainlanguage{hebrew}
\setotherlanguage{english}
\usepackage{fontspec}
\setmainfont{David CLM}           % or Frank Ruehl CLM
\usepackage{bidi}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{biblatex}
\addbibresource{refs.bib}
```

### 6.2 Required Structural Elements

| Element | Location | Requirement |
|---------|----------|-------------|
| **Cover Sheet** | Before `\tableofcontents` | Title (Hebrew), author, date, institution |
| **Table of Contents** | Page 2 | Auto-generated via `\tableofcontents` |
| **Headers/Footers** | All body pages | Chapter name in header (RTL), page number in footer — via `fancyhdr` |
| **Table** | Chapter 3 or 4 | `booktabs`-style table comparing model architectures (e.g., BERT vs GPT vs T5) |
| **Image** | Chapter 3 | `\includegraphics` of `assets/attention_complexity.png` |
| **Math Formula** | Chapter 2 | Numbered `equation` environment with Scaled Dot-Product Attention |
| **Bibliography** | Final pages | `\printbibliography`, minimum 6 BibTeX entries |

### 6.3 BibTeX Entries (minimum set)

The `refs.bib` must include entries for:

1. Vaswani et al., "Attention Is All You Need," NeurIPS 2017
2. Devlin et al., "BERT," NAACL 2019
3. Radford et al., "Language Models are Unsupervised Multitask Learners," OpenAI 2019
4. Brown et al., "Language Models are Few-Shot Learners," NeurIPS 2020
5. Bahdanau et al., "Neural Machine Translation by Jointly Learning to Align and Translate," ICLR 2015
6. Hochreiter & Schmidhuber, "Long Short-Term Memory," Neural Computation 1997

---

## 7. Skills Pattern — Specification

Skills are Markdown files under `skills/<name>/SKILL.md`. At crew construction time, `src/crew.py` reads each agent's designated skill file and sets it as the agent's `backstory`. No domain knowledge about LaTeX, Hebrew, or matplotlib may appear in `crew.py` itself.

### 7.1 Required Skill Files

| Skill Name | Injected Into | Purpose |
|------------|---------------|---------|
| `skills/manager/SKILL.md` | ManagerAgent | Delegation protocol, circuit-breaker escalation rules, hierarchical task ordering |
| `skills/perplexity-research/SKILL.md` | ResearcherAgent | Perplexity query strategies, citation extraction, research-notes Markdown format |
| `skills/academic-outline/SKILL.md` | OutlineAgent | Chapter planning conventions, JSON schema for outline |
| `skills/hebrew-academic-writing/SKILL.md` | ContentAgent | Hebrew academic register, `\textenglish{}` macro usage, RTL paragraph structure |
| `skills/lualatex-bidi/SKILL.md` | BidiAgent | LuaLaTeX bidi package rules, common RTL/LTR pitfalls, validation checklist |
| `skills/matplotlib-tikz/SKILL.md` | FigureAgent | matplotlib best practices (save as PNG 300dpi), TikZ syntax for formula diagrams |
| `skills/lualatex-build/SKILL.md` | CompilerAgent | `lualatex` CLI flags, 4-step pipeline strategy, log parsing, preamble assembly rules |

### 7.2 Skill Loading Contract

```python
# src/crew.py — the ONLY place skills are loaded
def _load_skill(name: str) -> str:
    path = Path(f"skills/{name}/SKILL.md")
    return path.read_text(encoding="utf-8")
```

Agents are constructed as:

```python
Agent(
    role=...,
    goal=...,
    backstory=_load_skill("lualatex-bidi"),  # skill injected here
    tools=[...],
    llm=settings.LLM_MODEL,
)
```

---

## 8. Tool Definitions

### 8.1 `latex_writer`

- **Input:** `path: str`, `content: str`, `mode: Literal["write", "append"]`
- **Behavior:** Writes UTF-8 encoded content to the given path under `latex_output/`. Creates parent directories. In `append` mode, adds a newline separator.
- **Constraint:** Path must be within `latex_output/` — raises `ValueError` on path traversal.

### 8.2 `python_runner`

- **Input:** `script: str` (Python source code as string)
- **Behavior:** Writes script to a temp file, executes via `subprocess.run(["python3", ...], timeout=60)`, captures stdout/stderr.
- **Constraint:** Script must not import anything outside `{matplotlib, numpy, pathlib, os}`. Validated by static import scan before execution.

### 8.3 `lualatex_runner`

- **Input:** `tex_file: str` (path to `.tex` file), `passes: int = 4`
- **Behavior:** Runs `lualatex --interaction=nonstopmode --output-directory=latex_output <tex_file>` N times. Parses `.log` for `! LaTeX Error` and raises `CompilationError` if found.
- **Returns:** `{"success": bool, "pdf_path": str, "log_tail": str}`

---

## 9. Configuration (`.env` / `config.py`)

All tuneable values must be in `.env` and loaded via `src/config.py` (pydantic-settings `Settings`). No magic numbers in any `.py` file.

| Setting | Type | Default | Purpose |
|---------|------|---------|---------|
| `LLM_MODEL` | str | `anthropic/claude-haiku-4-5-20251001` | CrewAI agent LLM (default); `LLM_MODEL_SMART` uses `anthropic/claude-sonnet-4-6` |
| `ANTHROPIC_API_KEY` | str | — | API key (never committed) |
| `MAX_AGENT_RETRIES` | int | 2 | Retry budget per agent task |
| `PYTHON_RUNNER_TIMEOUT_S` | int | 60 | Timeout for graph generation subprocess |
| `LUALATEX_BIN` | str | `lualatex` | Path to lualatex binary |
| `OUTPUT_DIR` | str | `latex_output` | Root output directory |
| `ASSETS_DIR` | str | `latex_output/assets` | Graph/image output directory |
| `MIN_PAGES` | int | 15 | Acceptance threshold for compiled page count |

---

## 10. Directory Structure (Target State)

```
crewai-latex-publisher/
├── CLAUDE.md
├── pyproject.toml
├── .env                          # not committed
├── .env.example                  # committed, no secrets
├── main.py                       # entry point: PublisherCrew().kickoff()
├── src/
│   ├── config.py                 # pydantic-settings Settings
│   ├── crew.py                   # CrewAI Crew definition, skill loading
│   ├── agents/
│   │   ├── outline_agent.py
│   │   ├── content_agent.py
│   │   ├── bidi_agent.py
│   │   ├── figure_agent.py
│   │   └── compiler_agent.py
│   ├── tasks/
│   │   ├── outline_task.py
│   │   ├── content_task.py
│   │   ├── bidi_task.py
│   │   ├── figure_task.py
│   │   └── compile_task.py
│   └── tools/
│       ├── latex_writer.py
│       ├── python_runner.py
│       └── lualatex_runner.py
├── skills/
│   ├── academic-outline/SKILL.md
│   ├── hebrew-academic-writing/SKILL.md
│   ├── lualatex-bidi/SKILL.md
│   ├── matplotlib-tikz/SKILL.md
│   └── lualatex-build/SKILL.md
├── tests/
│   ├── test_config.py
│   ├── test_latex_writer.py
│   ├── test_python_runner.py
│   ├── test_lualatex_runner.py
│   ├── test_crew.py
│   └── test_integration.py
├── docs/
│   ├── PRD.md                    ← this file
│   └── TODO.md
└── latex_output/                 # generated — gitignored except .gitkeep
    ├── assets/
    ├── chapters/
    ├── figures/
    ├── refs.bib
    └── main.tex
```

No Python source file in `src/` may exceed **150 lines**. If a module approaches the limit during implementation, split it.

---

## 11. Acceptance Criteria

### 11.1 Functional

- [ ] `python main.py` runs to completion without unhandled exceptions.
- [ ] `latex_output/main.pdf` exists after a successful run.
- [ ] PDF contains at least 15 pages (verified by `pdfinfo main.pdf | grep Pages`).
- [ ] All 6 chapters are present in the TOC.
- [ ] The Scaled Dot-Product Attention equation appears as a numbered equation.
- [ ] `assets/attention_complexity.png` is embedded in the PDF.
- [ ] The architecture comparison table is present in Chapter 3 or 4.
- [ ] Bibliography contains at least 6 entries and all are cited in the text.
- [ ] Chapter 3 contains mixed Hebrew/English BiDi text with no `bidi` package warnings in the `.log`.

### 11.2 Structural

- [ ] `uv run ruff check .` exits 0.
- [ ] `uv run pytest --cov=src` exits 0 with ≥80% coverage.
- [ ] `wc -l src/**/*.py` — no file exceeds 150 lines.
- [ ] All skills are loaded from `SKILL.md` files; no agent `backstory` is a hardcoded string in `.py` files.
- [ ] No value from the Configuration table (§9) appears as a literal in any `.py` file.

### 11.3 LaTeX Compilation

- [ ] 4-step LuaLaTeX + Biber run produces no `! LaTeX Error` lines.
- [ ] `\tableofcontents` resolves all chapter entries correctly.
- [ ] `hyperref` produces working internal links (TOC → chapter, citation → bibliography).

---

## 12. Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| LuaLaTeX not installed in CI | Medium | Document install in `README.md`; skip `test_lualatex_runner` with `pytest.mark.skipif` when binary absent |
| Hebrew font (David CLM) unavailable | Medium | Fallback chain in preamble: `David CLM`, then `Frank Ruehl CLM`, then `Noto Serif Hebrew` |
| Agent produces invalid LaTeX | High | BidiAgent validates fragments before compile; `lualatex_runner` raises `CompilationError` with log tail for retry |
| Token budget overflow (15-page book) | Medium | Each ContentAgent task covers exactly one chapter; `MAX_AGENT_RETRIES` caps runaway loops |
| `python_runner` script injection | Low | Static import whitelist enforced before execution; no user-supplied input reaches the script |

---

## 13. Out-of-Scope for This PRD

The following are explicitly deferred to future work and must not be implemented now:

- Automatic chapter regeneration on compilation failure (would require a feedback loop agent — scope creep).
- Support for figures beyond the one graph and one TikZ block.
- Hebrew spell-checking or grammar validation of agent output.
- Parallelization of chapter writing (sequential task ordering is simpler and sufficient).

---

## 14. Implementation Order (maps to `docs/TODO.md`)

1. `src/config.py` + `tests/test_config.py` — settings load from `.env`
2. `src/tools/latex_writer.py` + `tests/test_latex_writer.py`
3. `src/tools/python_runner.py` + `tests/test_python_runner.py`
4. `src/tools/lualatex_runner.py` + `tests/test_lualatex_runner.py`
5. All seven `SKILL.md` files under `skills/`
6. All seven agent modules + `src/crew.py` + `tests/test_crew.py`
7. All task modules (`research_task`, `outline_task`, `content_task`, `bidi_task`, `figure_task`, `figure_embed_task`, `compile_task`)
8. `latex_output/refs.bib`
9. End-to-end `tests/test_integration.py` (marked `slow`)
10. `main.py` wired to `PublisherCrew().kickoff()`

Every step: write failing test first, then implement.
