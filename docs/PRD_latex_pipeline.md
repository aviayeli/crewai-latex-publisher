# PRD — LaTeX Publisher Pipeline (Mechanism Reference)

**Version:** 1.0  
**Author:** Avi Ayeli  
**Status:** Production

---

## 1. Overview

This document describes the complete content-to-PDF conversion pipeline implemented
in the `crewai-latex-publisher` repository. The pipeline converts AI-generated
Markdown chapter drafts into a typeset Hebrew-English bilingual PDF using LuaLaTeX,
Polyglossia, and Biber.

---

## 2. End-to-End Pipeline Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  Perplexity Research (researcher_agent)                         │
│  → latex_output/raw/research_raw.md                            │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  Outline Planning (outline_agent)                               │
│  → latex_output/book_outline.json                              │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  Markdown Generation (content_agent, 6 chapters)                │
│  → latex_output/chapters/ch{1..6}.md                          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE A — Pandoc Conversion  (markdown_converter_tool)        │
│  → latex_output/chapters/ch{1..6}.tex                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE B — Regex Post-Processing  (_post_process)              │
│  Strip preamble noise + restore \textenglish{}                 │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  BiDi Validation (bidi_agent)                                   │
│  Validates all 6 chapters; inserts missing \textenglish{},     │
│  \begin{LTR}, \begin{english} constructs                       │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE C — 4-Step LuaLaTeX + Biber Compilation                │
│  Step 1: lualatex pass 1 → main.bcf, main.aux                 │
│  Step 2: biber         → main.bbl (resolved citations)        │
│  Step 3: lualatex pass 2 → main.pdf (cross-refs resolved)     │
│  Step 4: log parsing   → surface any ! LaTeX Error lines      │
│  → latex_output/main.pdf                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Stage A — Pandoc Conversion

**Tool:** `src/tools/markdown_converter.py` → `MarkdownConverterTool`

**CLI flags used:**

```
pandoc -f markdown+raw_tex -t latex --wrap=none -o <tex_path> <md_path>
```

| Flag | Rationale |
|---|---|
| `-f markdown+raw_tex` | Passes inline LaTeX (`\textenglish{}`, `\cite{}`) through unchanged |
| `-t latex` | Outputs a LaTeX fragment (no standalone preamble — chapter files are fragments) |
| `--wrap=none` | Prevents Hebrew Unicode codepoints from being line-wrapped |

**Path validation:** Both `md_path` and `tex_path` are validated to be relative
to `settings.OUTPUT_DIR` using `Path.is_relative_to()`. Any path that escapes
the output directory raises `ValueError` (path traversal protection).

---

## 4. Stage B — Regex Post-Processing

**Method:** `MarkdownConverterTool._post_process(tex_path)`

### 4.1 Preamble Noise Stripping

Pandoc in non-standalone mode still emits `\providecommand`, `\setlength`, and
`\hypertarget` lines that conflict with `main.tex`'s preamble. These are stripped
by filtering every line that starts with one of those prefixes.

### 4.2 `\textenglish{}` Unescaping

Pandoc mangles `\textenglish{X}` in two ways:

**Form 1 — code-span input** (`` `\textenglish{X}` `` in Markdown):
```
\texttt{\textbackslash{}textenglish\{X\}}
```

**Form 2 — double-backslash input** (`\\textenglish{X}` in Markdown):
```
\textbackslash textenglish\{X\}
```

Both are restored to `\textenglish{X}` by these compiled patterns:

```python
re.compile(r"\\texttt\{\\textbackslash\{\}textenglish\\{([^}\\]*)\\}\}")
→ r"\\textenglish{\1}"

re.compile(r"\\textbackslash\s+textenglish\\{([^}\\]*)\\}")
→ r"\\textenglish{\1}"
```

The patterns are applied sequentially after preamble stripping, never before.

---

## 5. Stage C — 4-Step LuaLaTeX + Biber Compilation

**Tool:** `src/tools/lualatex_runner.py` → `LualatexRunnerTool`

All binary paths are sourced from `settings` (never hardcoded):

| Setting | Default |
|---|---|
| `settings.LUALATEX_BIN` | `"lualatex"` |
| `settings.BIBER_BIN` | `"biber"` |
| `settings.OUTPUT_DIR` | `"latex_output"` |

### Step 1 — First LuaLaTeX Pass

```
lualatex --interaction=nonstopmode --output-directory=latex_output latex_output/main.tex
```

Produces `main.bcf` (Biber control file) and `main.aux`.

### Step 2 — Biber Pass

```
biber latex_output/main
```

Argument is the **stem** (no extension). Reads `main.bcf`, resolves all `\cite{}`
keys against `refs.bib`, writes `main.bbl`.

### Step 3 — Second LuaLaTeX Pass

```
lualatex --interaction=nonstopmode --output-directory=latex_output latex_output/main.tex
```

Reads `main.bbl` and resolves cross-references. Produces `main.pdf`.

### Step 4 — Log Parsing

After the final pass, `main.log` is scanned for lines beginning with `! `.
Any such line is extracted and raised as `CompilationError`. Warnings
(`Overfull`, `Warning:`) are non-fatal.

### HITL Gate (Optional)

When `settings.HITL_ENABLED=True`, the operator is prompted before Step 1:

```
[HITL] Press Y to execute the N-step PDF compilation for '<file>' [Y/n]:
```

Entering anything other than `Y` raises `RuntimeError` and aborts compilation.
Enable via `HITL_ENABLED=true` in `.env`.

---

## 6. `main.tex` Document Class and Preamble

```latex
\documentclass[17pt,a4paper]{extarticle}

\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{hebrew}
\setotherlanguage{english}

\usepackage[backend=biber,style=authoryear]{biblatex}
\addbibresource{refs.bib}

\usepackage{geometry}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{hyperref}
\usepackage{tikz}
\usepackage{booktabs}
\usepackage{xcolor}

\newfontfamily\hebrewfont[Script=Hebrew]{David CLM}
\setmonofont{Courier New}
\setsansfont{Arial}
```

**Why `extarticle`:** The 17pt font size option is not available in the standard
`article` class; `extarticle` extends the size range.

**Why `polyglossia` not `babel`:** `polyglossia` integrates with LuaLaTeX's
font renderer for proper RTL shaping. `babel` does not support LuaLaTeX RTL.

---

## 7. Source of Truth Locations

| Artifact | Path |
|---|---|
| Chapter Markdown | `latex_output/chapters/ch{1..6}.md` |
| Chapter LaTeX fragments | `latex_output/chapters/ch{1..6}.tex` |
| Main document | `latex_output/main.tex` |
| Bibliography | `latex_output/refs.bib` |
| Final PDF | `latex_output/main.pdf` |
| Book outline | `latex_output/book_outline.json` |
| Figures | `latex_output/figures/`, `latex_output/assets/` |

---

## 8. Configuration Contract

All tuneable values live in `.env` and are loaded via `src/config.py`
(`pydantic-settings`). No magic numbers appear in Python source files.

Key settings:

| Variable | Default | Purpose |
|---|---|---|
| `LLM_MODEL` | `anthropic/claude-haiku-4-5-20251001` | Model for all agents |
| `MAX_AGENT_RETRIES` | `3` | Hard circuit breaker (3 strikes = halt) |
| `MAX_ITER` | `15` | Max tool-call iterations per agent turn |
| `MAX_TOKENS` | `4096` | Hard output cap per LLM call |
| `LUALATEX_BIN` | `lualatex` | LuaLaTeX binary path |
| `BIBER_BIN` | `biber` | Biber binary path |
| `PANDOC_BIN` | `pandoc` | Pandoc binary path |
| `OUTPUT_DIR` | `latex_output` | Output directory for all artefacts |
| `HITL_ENABLED` | `false` | Enable operator approval gate before compilation |
| `MIN_PAGES` | `15` | Minimum page count for a valid output PDF |
