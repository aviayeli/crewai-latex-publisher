---
name: lualatex-build
description: Guides the LaTeX Build Engineer agent through the full Markdown-to-PDF pipeline for the Hebrew academic publisher. The agent first converts each chapter's Markdown source to LaTeX using Pandoc (via markdown_converter_tool), then assembles a complete main.tex preamble with all required packages for Hebrew BiDi, bibliography, and math support, and finally runs the three-step LuaLaTeX/Biber compilation sequence (lualatex → biber → lualatex) to produce a correctly typeset, citation-resolved 15-page PDF. This skill documents every CLI flag, package declaration, font fallback chain, binary path setting, and log-parsing heuristic the agent needs to execute the build reliably without human intervention.
metadata:
  author: Avi Ayeli
  version: "1.0"
---

# LaTeX Build Engineer

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

## Document Class Declaration

Every `main.tex` must begin with:

```latex
\documentclass[17pt,a4paper]{extarticle}
```

- `extarticle` is required for the `17pt` font size option (not available in the standard `article` class).
- `a4paper` sets the paper size to A4 (210 × 297 mm).

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
| `hyperref` | PDF hyperlinks and metadata |
| `tikz` | TikZ diagram support |
| `booktabs` | Publication-quality table rules |
| `xcolor` | Colour support |

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
```

---

## Complete `main.tex` Body Skeleton

The assembled `main.tex` must be written to `latex_output/main.tex` via `latex_writer_tool`. The body follows the preamble immediately after `\begin{document}`:

```latex
\begin{document}

\input{chapters/ch1}
\input{chapters/ch2}
\input{chapters/ch3}
\input{chapters/ch4}
\input{chapters/ch5}
\input{chapters/ch6}

\printbibliography

\end{document}
```

- `\input{}` paths are relative to `main.tex` location (`latex_output/`).
- `\printbibliography` must appear after the last `\input{}` and before `\end{document}`.
- Do not use `\include{}` — it forces a page break before each file. Use `\input{}` instead.

---

## Three-Step Biber Compilation Pipeline

Run these three commands in strict sequence:

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
- Produces the final `latex_output/main.pdf`.

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

Any line beginning with `! ` should be extracted and surfaced as a `CompilationError`. Lines beginning with `Warning:` or `Overfull` are non-fatal and do not block pipeline progression.

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
