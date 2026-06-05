---
name: latex-expert
description: >
  Consolidated LuaLaTeX expertise covering Hebrew BiDi configuration via
  Polyglossia, Courier New / Arial Latin font injection via fontspec, and
  the two-pattern Regex unescaping protocol that restores \textenglish{}
  commands mangled by Pandoc. Inject this skill into any agent that writes
  or post-processes .tex files so it has authoritative knowledge of the
  font stack and the Pandoc sanitisation pipeline.
metadata:
  author: Avi Ayeli
  version: "1.0"
---

# LaTeX Expert — Consolidated Pipeline Knowledge

This skill captures the three areas of hard-won expertise developed during
the production of the Hebrew-language Transformer academic book. Each section
is self-contained and actionable.

---

## 1. LuaLaTeX BiDi with Polyglossia

### Setup (preamble only — never in chapter files)

```latex
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{hebrew}
\setotherlanguage{english}
```

- **`polyglossia`** replaces `babel` for LuaLaTeX; using `babel` breaks RTL.
- **`bidi`** is loaded automatically by `polyglossia`; never add `\usepackage{bidi}` manually — it causes a "bidi already loaded" conflict.
- `\setmainlanguage{hebrew}` sets RTL as the document default direction.
- `\setotherlanguage{english}` registers English for `\textenglish{}` and `\begin{english}`.

### Inline LTR inside RTL paragraphs

| Scope | Command |
|---|---|
| Single word / phrase | `\textenglish{Transformer}` |
| Multi-line block | `\begin{english}…\end{english}` |
| Code / formula with brackets | `\begin{LTR}…\end{LTR}` |

**Rule:** brackets `(`, `[`, `<` inside RTL context are mirrored by bidi.
Wrap any expression containing paired delimiters in `\begin{LTR}` or
`\textenglish{}` to prevent mirroring artifacts.

---

## 2. Font Injection — Courier New (monospace) and Arial (sans-serif)

### Why these fonts

The academic template requires:
- **Courier New** — code listings, verbatim environments, terminal output.
- **Arial** — section headings and caption labels for a clean sans-serif look.

Both fonts must be declared via `fontspec` *before* `\begin{document}`.

### Declarations

```latex
% Monospace for code listings
\setmonofont{Courier New}

% Sans-serif for headings
\setsansfont{Arial}[
  BoldFont = Arial Bold,
  ItalicFont = Arial Italic,
  BoldItalicFont = Arial Bold Italic,
]
```

### Fallback chain

If `Arial` is not installed on the build system, substitute in order:

1. `Liberation Sans` (metrically compatible, available on Linux)
2. `Noto Sans`

For `Courier New` the fallback is:

1. `Liberation Mono`
2. `DejaVu Sans Mono`

### Hebrew font fallback chain

```latex
\newfontfamily\hebrewfont[Script=Hebrew]{David CLM}
% Fallback 1: Frank Ruehl CLM
% Fallback 2: Noto Serif Hebrew
```

All three fonts must be checked with `fc-list | grep -i "david\|frank\|noto"` on
the build system before the first compilation run.

---

## 3. Regex Unescaping — Restoring `\textenglish{}` After Pandoc

### Problem

Pandoc escapes `\textenglish{X}` in two different ways depending on how the
Markdown source wrote the backslash:

| Source form | Pandoc output |
|---|---|
| `` `\textenglish{X}` `` (code span) | `\texttt{\textbackslash{}textenglish\{X\}}` |
| `\\textenglish{X}` (double backslash) | `\textbackslash textenglish\{X\}` |

Both forms must be restored to `\textenglish{X}` so LaTeX renders the
command instead of printing it literally.

### Patterns (Python `re`)

```python
import re

_TEXTENGLISH_PATTERNS = [
    # code-span form: \texttt{\textbackslash{}textenglish\{X\}}
    (
        re.compile(r"\\texttt\{\\textbackslash\{\}textenglish\\{([^}\\]*)\\}\}"),
        r"\\textenglish{\1}",
    ),
    # double-backslash form: \textbackslash textenglish\{X\}
    (
        re.compile(r"\\textbackslash\s+textenglish\\{([^}\\]*)\\}"),
        r"\\textenglish{\1}",
    ),
]

for pattern, replacement in _TEXTENGLISH_PATTERNS:
    text = pattern.sub(replacement, text)
```

### Application point

Apply the patterns in `_post_process()` inside `MarkdownConverterTool`, after
stripping Pandoc preamble noise (`\providecommand`, `\setlength`, `\hypertarget`).
Never apply them before stripping — the preamble lines may also contain
`\textbackslash` tokens that should not be touched.

### Validation

After unescaping, grep the output `.tex` file for any remaining
`textbackslash.*textenglish` strings. If found, at least one pattern failed;
inspect the raw Pandoc output for a third escape form.

---

## 4. Pandoc CLI Flags for BiDi-Safe Conversion

```
pandoc -f markdown+raw_tex -t latex --wrap=none -o <out.tex> <in.md>
```

| Flag | Purpose |
|---|---|
| `-f markdown+raw_tex` | Pass inline LaTeX (`\textenglish{}`, `\cite{}`) through unchanged |
| `-t latex` | Output LaTeX fragment (no standalone preamble) |
| `--wrap=none` | Prevent Hebrew Unicode codepoints from being split across lines |

**Never** use `-s` / `--standalone` for chapter files — it injects a full
preamble that conflicts with `main.tex`.

---

## 5. Post-Processing Checklist

After every Pandoc conversion, verify:

1. No `\providecommand`, `\setlength`, or `\hypertarget` lines remain.
2. No `\textbackslash.*textenglish` strings remain (both patterns applied).
3. Chapter file does **not** contain `\begin{document}` — fragments only.
4. First non-blank content is `\chapter{…}`.
5. All `\begin{LTR}` are matched with `\end{LTR}`.
6. All `\begin{english}` are matched with `\end{english}`.
