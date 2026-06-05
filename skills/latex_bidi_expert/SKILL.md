---
name: latex-bidi-expert
description: >
  Guides the Converter Agent in safely transforming Hebrew Markdown to
  LuaLaTeX fragments with correct Polyglossia BiDi directives,
  mandatory \textenglish{} wrapping for all inline English, and
  proper Pandoc post-processing to eliminate escape artifacts.
metadata:
  author: Avi Ayeli
  version: "1.0"
  skill_spec: "S = <C, π, T, R>"
---

# LaTeX BiDi Expert — Formal Skill Specification (S = <C, π, T, R>)

---

## C — Applicability Conditions

Activate when **all** hold:

1. Converting a Markdown chapter file to a `.tex` fragment via `markdown_converter_tool`.
2. The document preamble contains `\setmainlanguage{hebrew}` (RTL default).
3. The chapter body contains mixed Hebrew–English content (BiDi text).

**Do NOT apply** to standalone English-only appendices, bibliography `.bib` files,
or TikZ figure files that contain no Hebrew text.

---

## π — Execution Policy

### 1. Polyglossia Configuration (preamble — not in chapter files)

The main document preamble (`main.tex`) must contain:

```latex
\usepackage{polyglossia}
\setmainlanguage{hebrew}
\setotherlanguage{english}
```

**CRITICAL:** Never add `\usepackage{bidi}` manually.
Polyglossia loads `bidi` automatically; a manual load causes
"bidi already loaded" conflict error under LuaLaTeX.

### 2. Mandatory Inline English Wrapping: `\textenglish{}`

Every Latin-script word inside a Hebrew RTL paragraph **must** be wrapped:

```latex
ארכיטקטורת \textenglish{Transformer} מבוססת על מנגנון תשומת לב עצמית.
```

Wrap these categories without exception:
- Model names: `Transformer`, `BERT`, `GPT`, `xLSTM`, `RNN`, `LSTM`
- Acronyms in Latin script: `NLP`, `GPU`, `API`, `MCP`, `BiDi`
- Mathematical variable names in prose: `\textenglish{Q}`, `\textenglish{d_k}`

### 3. Multi-Line English Blocks: `\begin{english}…\end{english}`

For ≥ 2 consecutive LTR lines (abstracts, long quotations):

```latex
\begin{english}
The attention mechanism computes a weighted sum over values.
\end{english}
```

### 4. Code and Formula Blocks: `\begin{LTR}…\end{LTR}`

Wrap all `verbatim`, `equation`, pseudocode, and table blocks containing
brackets or arrows in `\begin{LTR}`:

```latex
\begin{LTR}
\begin{verbatim}
scores = (Q @ K.T) / math.sqrt(d_k)
\end{verbatim}
\end{LTR}
```

This prevents `bidi` from mirroring `(`, `[`, `<` inside RTL context.

### 5. Pandoc Post-Processing (via `markdown_converter_tool`)

After conversion, the tool automatically:
- Strips `\providecommand`, `\setlength`, `\hypertarget` preamble noise.
- Unescapes `\textenglish{}` from two Pandoc mangling forms:
  - `\texttt{\textbackslash{}textenglish\{X\}}` → `\textenglish{X}`
  - `\textbackslash textenglish\{X\}` → `\textenglish{X}`

Verify post-processing succeeded: `grep -n 'textbackslash.*textenglish'` must return empty.

---

## T — Termination Criteria

Conversion is complete when **all** hold:

1. No bare `$…$` inline math remains (all math uses `\(…\)` or `\begin{equation}`).
2. All English model names and acronyms are inside `\textenglish{}`.
3. No unclosed `\begin{LTR}` or `\begin{english}` environments.
4. `\begin{document}` does **not** appear in any chapter fragment file.
5. No `\textbackslash.*textenglish` escape artifacts remain in the `.tex` output.
6. Chapter file begins with `\chapter{…}` as its first non-blank content.

---

## R — Callable Interface

| Tool / Command | Usage |
|---|---|
| `markdown_converter_tool(md_path, tex_path)` | Convert Markdown to LaTeX fragment |
| `latex_writer_tool(path, mode, content)` | Patch specific lines in the `.tex` file |
| `\textenglish{word}` | Inline LTR switch for a single term |
| `\begin{LTR}…\end{LTR}` | Block LTR switch for code / math / tables |
| `\begin{english}…\end{english}` | Multi-line LTR switch |

**Boundary:** Do NOT modify `main.tex` preamble from within a chapter conversion task.
Preamble management is the CompilerAgent's exclusive responsibility.
