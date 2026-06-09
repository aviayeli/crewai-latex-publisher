---
name: lualatex-build
description: Guides the LaTeX Build Engineer agent through the full Markdown-to-PDF pipeline for the Hebrew academic publisher. The agent first converts each chapter's Markdown source to LaTeX using Pandoc (via markdown_converter_tool), then assembles a complete main.tex preamble with all required packages for Hebrew BiDi, bibliography, and math support, and finally runs the three-step LuaLaTeX/Biber compilation sequence (lualatex → biber → lualatex) to produce a correctly typeset, citation-resolved 15-page PDF. This skill documents every CLI flag, package declaration, font fallback chain, binary path setting, and log-parsing heuristic the agent needs to execute the build reliably without human intervention.
metadata:
  author: Avi Ayeli
  version: "1.0"
---

# LaTeX Build Engineer

## CRITICAL: STEP 0 — Audit and Repair `templates/preamble.tex` BEFORE Anything Else

**FIRST ACTION** — before running pandoc, lualatex, or any other tool, you MUST audit `templates/preamble.tex` and repair it if stale.

### Audit Checklist

Read `templates/preamble.tex` and verify ALL of the following lines are present:

| Required line | Missing? → Action |
|---|---|
| `\usepackage{tikz}` | If missing: repair preamble immediately (see below) |
| `\documentclass[12pt,a4paper]{report}` | If wrong class: repair preamble immediately |
| `\usepackage{fancyhdr}` | If missing: repair preamble immediately |
| `\addbibresource{refs.bib}` | If missing: repair preamble immediately |

### If Any Required Line Is Missing — Overwrite preamble.tex Now

Use `latex_writer_tool` in `write` mode to overwrite `templates/preamble.tex` with the EXACT content from the "Complete Preamble Skeleton" section in this SKILL.md. Do NOT use the old preamble.tex content — replace it entirely.

```
tool: latex_writer_tool
path: templates/preamble.tex
mode: write
content: <paste exact content of Complete Preamble Skeleton from this SKILL.md>
```

After writing the corrected preamble, emit: `[CHECKPOINT] STEP 0 complete: templates/preamble.tex repaired — \usepackage{tikz} confirmed.`

Only AFTER completing STEP 0 may you proceed to pandoc conversion and lualatex compilation.

---

## Role

The LaTeX Build Engineer agent is responsible for two sequential operations:

1. **Markdown → LaTeX conversion** — invoke `markdown_converter_tool` (which calls `pandoc`) to convert each chapter `.md` file into a `.tex` file.
2. **LaTeX → PDF compilation** — assemble `main.tex`, then run the three-step LuaLaTeX/Biber pipeline to produce `latex_output/main.pdf`.

The agent operates only on files that already exist on disk. It never writes Hebrew prose or generates figure content — that is the responsibility of upstream agents.

---

## Markdown-First Workflow

The content pipeline follows a Markdown-first strategy:

1. `content_agent` writes each chapter as `latex_output/chapters/ch{n}.md` using `latex_writer_tool`.
2. `content_agent` calls `markdown_converter_tool` (pandoc) to convert each `.md` to `latex_output/chapters/ch{n}.tex`.
3. The Compiler Agent (`lualatex_runner_tool`) operates **only** on the resulting `.tex` files — it never reads `.md` files directly.

### Pandoc Invocation

The `markdown_converter_tool` calls pandoc with the following flags:

```
pandoc -f markdown -t latex -o <tex_path> <md_path>
```

- `-f markdown` — input format is standard Markdown.
- `-t latex` — output format is LaTeX.
- `-o <tex_path>` — write output to the resolved `.tex` path.

The binary path is sourced from `settings.PANDOC_BIN` (default: `"pandoc"`). Never hardcode the binary path.

---

## CRITICAL: Document Class — ALWAYS `report`/`12pt`, NEVER `extarticle`/`17pt`

Every `main.tex` and `templates/preamble.tex` must begin with:

```latex
\documentclass[12pt,a4paper]{report}
```

- `report` is the correct class for a multi-chapter Hebrew academic document.
- `12pt` is the correct font size — do NOT use `17pt`.
- NEVER use `extarticle` — it is incompatible with the `\chapter{}` command used by all six chapter files.
- NEVER use `article`, `book`, or any other class.

---

## CRITICAL: Cover Page — Logical Hebrew Author Name, AI Watermark, Empty Page Style

The cover page (inside `\begin{titlepage}...\end{titlepage}`) must contain ALL of the following:

1. **Author name in LOGICAL Hebrew order**: `אבי איילי` — NEVER write `ילייא יבא` (reversed).
   - Correct: `\author{אבי איילי --- ת.ז. \textenglish{300228160}}`
   - The abbreviation MUST be `ת.ז.` (with the period after each letter).
2. **AI-generation watermark** — the cover page body must include this exact line:
   ```latex
   {\small מסמך זה נוצר בסיוע בינה מלאכותית\par}
   ```
3. **Empty page style on the cover** — the very first command after `\begin{titlepage}` must be:
   ```latex
   \thispagestyle{empty}
   ```
   This suppresses headers and footers on the cover page only.

---

## CRITICAL: Headers and Footers — ALWAYS `fancyhdr`, NEVER `\textdir TLT`

Load `fancyhdr` in the preamble:

```latex
\usepackage{fancyhdr}
\setlength{\headheight}{15pt}
```

Then configure headers and footers using `\AfterEndPreamble` (from etoolbox) — **NOT** `\AtBeginDocument`.
`\AfterEndPreamble` fires after ALL package hooks including polyglossia/luabidi, so the pagestyle cannot be reset by any subsequent package initialisation:

```latex
\makeatletter
\AfterEndPreamble{%
  \pagestyle{fancy}%
  \fancyhf{}%
  \fancyhead[R]{\@title}%
  \fancyfoot[C]{\thepage}%
  \renewcommand{\headrulewidth}{0.4pt}%
  \renewcommand{\footrulewidth}{0pt}%
  \fancypagestyle{plain}{%
    \fancyhf{}%
    \fancyhead[R]{\@title}%
    \fancyfoot[C]{\thepage}%
    \renewcommand{\headrulewidth}{0.4pt}%
    \renewcommand{\footrulewidth}{0pt}%
  }%
}
\makeatother
```

**WHY `\AfterEndPreamble`, not `\AtBeginDocument`:**
`\AtBeginDocument` runs as part of LaTeX's `begindocument` hook queue.
Polyglossia registers its own hooks in that same queue (to activate RTL bidi),
and those hooks fire AFTER ours — silently resetting `\pagestyle` and wiping the
`plain` override. `\AfterEndPreamble` (etoolbox) fires at the very end of
`\begin{document}` after every package has completed its setup, so the fancy
pagestyle and plain override are guaranteed to survive.

**FORBIDDEN patterns:**
- `\textdir TLT \thepage` — `\textdir` is a LuaTeX direction primitive, not a fancyhdr command. It produces `! Undefined control sequence` errors.
- `\def\ps@plain{...}` — low-level override; incompatible with fancyhdr active at document level.
- `\fancyfoot[C]{\textdir TLT \thepage}` — same as the first forbidden pattern above.

**The footer MUST be exactly:** `\fancyfoot[C]{\thepage}` — nothing else.

---

## CRITICAL: `\addbibresource` — Exactly Once in `templates/preamble.tex`

`templates/preamble.tex` MUST contain exactly this line:

```latex
\addbibresource{refs.bib}
```

`build_articles.py` MUST NOT inject an additional `\addbibresource` line when assembling articles. The function `_main_tex()` must build its `parts` list WITHOUT the addbibresource line — the preamble already supplies it.

**Forbidden pattern in `build_articles.py`:**
```python
# FORBIDDEN — causes Biber fatal error "found duplicate resource 'refs.bib'"
parts = [preamble, f"\\addbibresource{{{bib}}}\n", meta, ...]
```

**Required pattern:**
```python
# CORRECT — preamble.tex already declares \addbibresource
parts = [preamble, meta, ...]
```

Biber crashes with `FATAL - Error: Found duplicate resource 'refs.bib'` when `\addbibresource` appears twice.

---

## CRITICAL: BiDi Section-Number Reversal — `\renewcommand` Required

In RTL documents, section numbers like `1.3` render as `3.1` without explicit counter wrapping. `templates/preamble.tex` and `main.tex` MUST include:

```latex
\renewcommand{\thechapter}{\textenglish{\arabic{chapter}}}
\renewcommand{\thesection}{\textenglish{\arabic{chapter}.\arabic{section}}}
\renewcommand{\thesubsection}{\textenglish{\arabic{chapter}.\arabic{section}.\arabic{subsection}}}
```

These MUST appear after `\usepackage{biblatex}` and before `\begin{document}`.

---

## CRITICAL: BiDi Headers — NEVER Bare English Words in `\fancyhead`

In RTL headers, bare English words are subject to the BiDi algorithm and render reversed (the infamous "eltit" bug where `\title` renders letter-by-letter in RTL order).

**Wrong:**
```latex
\fancyhead[R]{My Title}  % renders as "eltiT yM"
```

**Correct:**
```latex
\fancyhead[R]{\@title}   % \@title is stored as a Hebrew string — safe
```

Or for English words in header:
```latex
\fancyhead[L]{\textenglish{Chapter \thechapter}}
```

---

## CRITICAL: `\printbibliography` — Mandatory in `main.tex`

Every assembled `main.tex` MUST contain `\printbibliography` as the last command before `\end{document}`:

```latex
\printbibliography

\end{document}
```

Without `\printbibliography`, the bibliography section is silently dropped from the PDF even when Biber runs successfully.

---

## CRITICAL: PDF Must Pass Through `.gitignore` for CI Verification

Add the following negation to `.gitignore` after the glob that ignores PDFs:

```gitignore
latex_output/*.pdf
!latex_output/main.pdf
```

This un-ignores `latex_output/main.pdf` specifically so GitHub Actions can upload it as a workflow artifact. Without this, CI cannot verify that the PDF was actually generated.

---

## Document Class Declaration

---

## Required Preamble Packages

Load the following packages in this order in the preamble:

| Package | Purpose |
|---|---|
| `fontspec` | OpenType font selection for LuaLaTeX |
| `polyglossia` | Multilingual support with BiDi; replaces `babel` |
| `biblatex` | Citation and bibliography management |
| `geometry` | Page margin control |
| `graphicx` | PNG/PDF figure inclusion |
| `amsmath` | Display math environments |
| `amssymb` | Extended math symbols |
| `hyperref` | PDF hyperlinks and metadata |
| `tikz` | TikZ block-diagram support |
| `booktabs` | Publication-quality table rules |
| `xcolor` | Colour support |
| `float` | Figure placement control (`[H]`) |
| `etoolbox` | Internal LaTeX patching |
| `fancyhdr` | Headers and footers (MANDATORY) |

**Important:** `polyglossia` must be used as the language package. Using `babel` instead of `polyglossia` will break Hebrew BiDi rendering under LuaLaTeX.

---

## Hebrew Font Fallback Chain

Configure `fontspec` to use Hebrew fonts in this priority order:

```latex
\newfontfamily\hebrewfont[Script=Hebrew]{David CLM}
% Fallback 1: Frank Ruehl CLM
% Fallback 2: Noto Serif Hebrew
```

If `David CLM` is not installed, LuaLaTeX will fall back to `Frank Ruehl CLM`, then `Noto Serif Hebrew`. At least one of these three fonts must be present on the build system.

---

## Language Configuration with Polyglossia

```latex
\setmainlanguage{hebrew}
\setotherlanguage{english}
```

- `\setmainlanguage{hebrew}` — sets Hebrew as the document default; text direction is RTL by default.
- `\setotherlanguage{english}` — registers English as a secondary language; use `\textenglish{}` or `\begin{english}...\end{english}` for LTR passages.

---

## Bibliography Configuration

```latex
\usepackage[backend=biber,style=authoryear]{biblatex}
\addbibresource{refs.bib}
```

- `backend=biber` is mandatory. Using `backend=bibtex` will break the pipeline because `biblatex` features (e.g., Unicode, `\printbibliography`) require Biber.
- `\addbibresource{refs.bib}` registers the bibliography database. The path is relative to `main.tex`.

---

## Complete Preamble Skeleton

```latex
\documentclass[12pt,a4paper]{report}

\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{hebrew}
\setotherlanguage{english}

\usepackage[backend=biber,style=numeric,language=english]{biblatex}

% BiDi section-number fix — MUST appear before \begin{document}
\renewcommand{\thechapter}{\textenglish{\arabic{chapter}}}
\renewcommand{\thesection}{\textenglish{\arabic{chapter}.\arabic{section}}}
\renewcommand{\thesubsection}{\textenglish{\arabic{chapter}.\arabic{section}.\arabic{subsection}}}

\usepackage[margin=2.5cm]{geometry}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{hyperref}
\usepackage{float}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{etoolbox}
\usepackage{fancyhdr}
\usepackage{tikz}

\setlength{\headheight}{15pt}

% Hebrew fonts (Windows / WSL path)
\setmainfont[Path=/mnt/c/Windows/Fonts/,Extension=.ttf,
  UprightFont=arial,BoldFont=arialbd,Script=Hebrew]{Arial}
\newfontfamily\hebrewfont[Path=/mnt/c/Windows/Fonts/,Extension=.ttf,
  UprightFont=arial,BoldFont=arialbd,Script=Hebrew]{Arial}

\addbibresource{refs.bib}

% Cover page metadata — logical Hebrew author name REQUIRED
\title{<כותרת המאמר>}
\author{אבי איילי --- ת.ז. \textenglish{300228160}}
\date{\today}

% fancyhdr — active on all pages except the cover
\makeatletter
\AtBeginDocument{%
  \pagestyle{fancy}%
  \fancyhf{}%
  \fancyhead[R]{\@title}%
  \fancyfoot[C]{\thepage}%
  \renewcommand{\headrulewidth}{0.4pt}%
  \fancypagestyle{plain}{%
    \fancyhf{}%
    \fancyhead[R]{\@title}%
    \fancyfoot[C]{\thepage}%
    \renewcommand{\headrulewidth}{0.4pt}%
  }%
}
\makeatother
```

The `\title`, `\author`, and `\date` lines **must appear before `\begin{document}`**. The `\author` field MUST use the logical Hebrew name `אבי איילי` (NEVER reversed).

---

## Complete `main.tex` Body Skeleton

The assembled `main.tex` must be written to `latex_output/main.tex` via `latex_writer_tool`. The body follows the preamble immediately after `\begin{document}`:

```latex
\begin{document}

% Cover page — MUST suppress headers/footers with \thispagestyle{empty}
\begin{titlepage}
\thispagestyle{empty}
\begin{hebrew}
\begin{center}
\vspace*{3cm}
{\bfseries\LARGE <כותרת המאמר>\par}
\vspace{1.5cm}
{\large אבי איילי --- ת.ז. \textenglish{300228160}\par}
{\large קורס: אורקסטרציה של סוכני \textenglish{AI}\par}
{\large מרצה: ד"ר יורם סגל\par}
{\large \textenglish{\the\year}\par}
\vspace{1.5cm}
{\small מסמך זה נוצר בסיוע בינה מלאכותית\par}
\end{center}
\end{hebrew}
\end{titlepage}

\tableofcontents
\newpage

\input{chapters/ch1}
\input{chapters/ch2}
\input{chapters/ch3}
\input{chapters/ch4}
\input{chapters/ch5}
\input{chapters/ch6}

\printbibliography

\end{document}
```

- **`\thispagestyle{empty}`** — MANDATORY first command inside `\begin{titlepage}` to suppress headers/footers on the cover page.
- **`\tableofcontents`** — generates the table of contents. Must appear after the titlepage.
- **`\newpage`** — separates the table of contents from chapter 1.
- `\input{}` paths are relative to `main.tex` location (`latex_output/`).
- **`\printbibliography`** — MANDATORY; must appear after the last `\input{}` and before `\end{document}`.
- Do not use `\include{}` — it forces a page break before each file. Use `\input{}` instead.

---

## Four-Pass LuaLaTeX Compilation Pipeline

Run these five commands in strict sequence (4 lualatex passes total):

### Step 1 — First LuaLaTeX Pass

```
lualatex --interaction=nonstopmode --output-directory=latex_output latex_output/main.tex
```

- Generates `latex_output/main.bcf` (Biber control file) and `latex_output/main.aux`.
- `--interaction=nonstopmode` prevents the process from pausing on errors; errors are recorded in the log instead.
- `--output-directory=latex_output` writes all auxiliary files (`.aux`, `.bcf`, `.log`, `.pdf`) into `latex_output/`.

### Step 2 — Biber Pass

```
biber latex_output/main
```

- The argument is the **stem** of the `.tex` file (no extension, no directory path prefix after `latex_output/`).
- Reads `latex_output/main.bcf`, resolves all `\cite{}` keys against `refs.bib`, writes `latex_output/main.bbl`.
- The binary path is sourced from `settings.BIBER_BIN` (default: `"biber"`).

### Step 3 — Second LuaLaTeX Pass

```
lualatex --interaction=nonstopmode --output-directory=latex_output latex_output/main.tex
```

- Reads `latex_output/main.bbl` and incorporates resolved bibliography entries.
- Resolves cross-references (`\ref{}`, `\pageref{}`) that could not be resolved in the first pass.

### Step 4 — Third LuaLaTeX Pass

```
lualatex --interaction=nonstopmode --output-directory=latex_output latex_output/main.tex
```

- Stabilises the Table of Contents page numbers and all `\pageref{}` targets.
- Ensures hyperref clickable links point to the correct final page offsets.

### Step 5 — Fourth LuaLaTeX Pass

```
lualatex --interaction=nonstopmode --output-directory=latex_output latex_output/main.tex
```

- Final convergence pass. Confirms all labels, TOC entries, and bibliography back-references are fully resolved.
- Produces the final `latex_output/main.pdf`.

**Why 4 passes?** Hebrew RTL documents with a Table of Contents and biblatex bibliography require more passes to converge than typical LTR documents: the TOC page numbers shift when the bibliography is inserted, and the bibliography itself can shift section page numbers. Four passes guarantee convergence for documents of 15+ pages.

---

## LuaLaTeX CLI Flags

| Flag | Purpose |
|---|---|
| `--interaction=nonstopmode` | Never pause on errors; log them and continue to end of file |
| `--output-directory=<dir>` | Write all output files (`.pdf`, `.log`, `.aux`, `.bcf`, `.bbl`) to `<dir>` |

Both flags are mandatory on every `lualatex` invocation. The binary path is sourced from `settings.LUALATEX_BIN` (default: `"lualatex"`).

---

## Configurable Binary Paths

Never hardcode binary paths in Python source. These are loaded from `settings`:

| Setting field | Default value | Purpose |
|---|---|---|
| `LUALATEX_BIN` | `"lualatex"` | Path to the LuaLaTeX binary |
| `BIBER_BIN` | `"biber"` | Path to the Biber binary |
| `PANDOC_BIN` | `"pandoc"` | Path to the pandoc binary |

---

## Output File Location

The assembled `main.tex` must be written to exactly:

```
latex_output/main.tex
```

All chapter `.tex` files must reside in:

```
latex_output/chapters/ch{n}.tex   (n = 1 … 6)
```

---

## Log Parsing Heuristics

After each LuaLaTeX pass, parse `latex_output/main.log` for error indicators. A line signals a fatal error if it begins with:

- `! LaTeX Error` — package or command error.
- `! Undefined control sequence` — a macro was used that was never defined.

Any line beginning with `! ` is a fatal error and raises `CompilationError`. Lines beginning with `LaTeX Warning:`, `Package <name> Warning:`, or `Class <name> Warning:` are surfaced in the error report for agent context but do not independently block pipeline progression.

---

## Context Purification — Log Trimming

**NEVER return the full raw `.log` output to the Writer agent.** A typical LuaLaTeX log is thousands of lines of binary metadata, font metrics, and path lookups. Returning it verbatim saturates the context window and causes O(n²) token growth.

When a compilation fails, `lualatex_runner_tool` already applies context purification automatically — it surfaces only lines matching `! ` (fatal) or named `Warning:` patterns. Your task as the Compiler Agent is to relay **only those purified lines** in your corrective feedback. Do not append, paraphrase, or reference any other section of the raw log.

---

## Circuit Breaker — Compilation Retry Limit

The Compiler Agent enforces a **hard limit of `settings.MAX_AGENT_RETRIES` fix-and-retry cycles** per article. With the current default of 2, the sequence is:

1. **Attempt 1** — run compilation; if it fails, relay the purified error lines and a SkillOpt directive to the Writer for a targeted fix.
2. **Attempt 2** — apply the fix, recompile; if it still fails, escalate immediately.
3. **Escalation** — do NOT attempt a third compile. Report the exact purified error lines to the Manager Agent and mark the task failed with `[CIRCUIT BREAKER TRIPPED]` in the output.

**Violation pattern to avoid:**
```
# FORBIDDEN — looping beyond MAX_AGENT_RETRIES
while compilation_fails:
    request_fix()
    recompile()
```

If the Manager re-delegates after escalation, treat that as Attempt 1 of a fresh cycle.

---

## Chapter `\input{}` Ordering Convention

Chapters must be `\input`-ed in ascending numeric order:

```
\input{chapters/ch1}   % Introduction to Transformers
\input{chapters/ch2}   % Transformer Architecture Deep Dive
\input{chapters/ch3}   % BiDi Text in Academic Publishing
\input{chapters/ch4}   % Applications and Fine-Tuning
\input{chapters/ch5}   % Evaluation Methodologies
\input{chapters/ch6}   % Conclusion and Future Work
```

Do not alter the order. Chapter 3 contains the mandatory BiDi constructs that depend on `polyglossia` language switching established in the preamble.
