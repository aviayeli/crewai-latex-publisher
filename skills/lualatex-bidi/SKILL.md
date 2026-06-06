---
name: lualatex-bidi
description: Configures LuaLaTeX for proper Hebrew and bidirectional (BiDi) text support by setting up polyglossia language directives (\setmainlanguage{hebrew}, \setotherlanguage{english}), managing the automatically-loaded bidi package, applying \textenglish{} for inline English inside RTL paragraphs, using \begin{english}...\end{english} for multi-line LTR blocks, and \begin{LTR}...\end{LTR} for code or data blocks; validates all six chapter files for BiDi correctness and inserts missing constructs without breaking surrounding context.
metadata:
  author: Avi Ayeli
  version: "1.0"
---

# LaTeX BiDi Typesetting Specialist

## Agent Role

The BiDi Typesetting Specialist validates and enforces correct bidirectional text rendering across all six chapter files. It reads each `.tex` file, identifies missing or malformed BiDi constructs, and overwrites the file in-place via `latex_writer_tool` with the corrected content.

---

## The `bidi` Package

The `bidi` package is **not loaded directly**. When `polyglossia` is loaded and Hebrew is set as the main language, `bidi` is automatically activated. Never add `\usepackage{bidi}` manually — this produces a "bidi already loaded" conflict error under LuaLaTeX.

---

## Language Configuration with `polyglossia`

Place these two declarations in the preamble, after `\usepackage{polyglossia}`:

```latex
\setmainlanguage{hebrew}
\setotherlanguage{english}
```

- `\setmainlanguage{hebrew}` sets the document direction to RTL globally.
- `\setotherlanguage{english}` registers English as the secondary language for inline switches.

---

## Inline English Inside Hebrew Paragraphs: `\textenglish{}`

Use `\textenglish{}` for any English word, phrase, or proper noun embedded within a Hebrew RTL paragraph:

```latex
הארכיטקטורה של \textenglish{Transformer} מבוססת על מנגנון תשומת הלב.
```

Rules:
- Model names (Transformer, BERT, GPT, LLaMA) are **never** translated; always wrapped in `\textenglish{}`.
- Acronyms in Latin script (NLP, AI, GPU) must use `\textenglish{}`.
- Mathematical variable names within prose (e.g., "המטריצה \textenglish{Q}") use `\textenglish{}`.

---

## Multi-Line English Blocks: `\begin{english}...\end{english}`

For multi-line English passages (abstracts, quotations, captions in English):

```latex
\begin{english}
The attention mechanism computes a weighted sum of values, where the weight
assigned to each value is determined by a compatibility function of the query
with the corresponding key.
\end{english}
```

---

## LTR Code and Data Blocks: `\begin{LTR}...\end{LTR}`

For source code listings, pseudocode, tables with Latin data, or any left-to-right block that must not be mirrored:

```latex
\begin{LTR}
\begin{verbatim}
attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
\end{verbatim}
\end{LTR}
```

This environment prevents bidi from mirroring parentheses, brackets, and arrow operators.

---

## Three Mandatory BiDi Constructs in Chapter 3

Chapter 3 ("דו-כיווניות") is the BiDi showcase chapter. It **must** contain all three of:

1. **RTL paragraph with inline `\textenglish{}`** — at least one Hebrew paragraph that wraps an English term using `\textenglish{}`.
2. **`\begin{equation}` environment** — display math inside an equation block (not bare `$$` or `\[`).
3. **`\begin{LTR}...\end{LTR}` block** — at least one left-to-right code or formula block.

The BidiAgent must insert any missing construct without removing surrounding Hebrew content.

---

## Two Mandatory Structural Elements Across All Chapters

In addition to the chapter-3 BiDi constructs, the following elements must exist somewhere across the six chapters:

### 1. Complexity Plot (`\includegraphics`)

At least one chapter must embed the pre-generated PNG via a `figure` environment:

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.85\textwidth]{latex_output/assets/attention_complexity.png}
    \caption{השוואת מורכבות חישובית: תשומת לב סטנדרטית \textenglish{O(n²)},
             תשומת לב לינארית \textenglish{O(n \log n)}, ורקורנטי \textenglish{O(n)}.}
    \label{fig:attention_complexity}
\end{figure}
```

If missing from all chapters, insert it into `ch2.tex` immediately after its first `\section{}` heading.

### 2. Model Comparison Table (`\begin{table}`)

At least one chapter must contain a `table` environment with a model comparison. Minimum required columns: **Model**, **Parameters**, **BLEU/Accuracy**, **Notes**.

```latex
\begin{table}[htbp]
    \centering
    \caption{השוואת מודלי שפה מרכזיים}
    \label{tab:model_comparison}
    \begin{LTR}
    \begin{tabular}{llll}
        \toprule
        Model & Parameters & Score & Notes \\
        \midrule
        \textenglish{BERT-base}  & 110M & 88.5 GLUE & Encoder-only \\
        \textenglish{GPT-3}      & 175B & 64.3 BIG-G & Decoder-only \\
        \textenglish{T5-large}   & 770M & 89.7 GLUE  & Encoder–Decoder \\
        \textenglish{LLaMA-2-7B} & 7B   & 63.2 MMLU  & Decoder-only \\
        \bottomrule
    \end{tabular}
    \end{LTR}
\end{table}
```

If missing from all chapters, insert it into `ch4.tex` immediately after its first `\section{}` heading.

---

## Common RTL/LTR Pitfall: Punctuation Mirroring Artifacts

In BiDi mode, LuaLaTeX mirrors certain characters: `(` becomes `)`, `[` becomes `]`, and `<` becomes `>` when they appear in RTL context.

**Broken (artifact):**
```latex
הפונקציה \textenglish{softmax(x)} מחזירה התפלגות הסתברות.
```
The parentheses around `x` may be mirrored because the RTL paragraph context leaks into the argument.

**Fix:** Wrap the entire inline expression including punctuation:
```latex
הפונקציה \textenglish{softmax(x)} מחזירה התפלגות הסתברות.
```
Or use `\begin{LTR}` for any expression containing paired delimiters:
```latex
\begin{LTR}$\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}$\end{LTR}
```

---

## Validation Checklist (12 Items — All 6 Chapters)

The BidiAgent must verify each of the following before marking a chapter as BiDi-clean:

1. **`\setmainlanguage{hebrew}` present in preamble** — not in the chapter file itself; verify `main.tex` contains it.
2. **No bare `$...$` inline math** — all inline math uses `\(` and `\)`.
3. **No bare `$$...$$` display math** — all display math uses `\begin{equation}` or `\begin{equation*}`.
4. **All English model names wrapped in `\textenglish{}`** — grep for unescaped Latin strings longer than 3 characters in Hebrew paragraphs.
5. **No mirrored parentheses in LTR expressions** — any formula or code containing `(`, `[`, or `<` inside RTL context is wrapped in `\begin{LTR}` or `\textenglish{}`.
6. **`\begin{english}` used for paragraphs ≥ 2 lines in English** — do not use `\textenglish{}` for multi-line spans.
7. **Chapter file does NOT contain `\begin{document}`** — chapter files are fragments, not standalone documents.
8. **Chapter begins with `\chapter{...}`** — no other sectioning command is the first non-blank content.
9. **`\begin{LTR}` has matching `\end{LTR}`** — no unclosed LTR environments (causes all subsequent text to render LTR).
10. **`\begin{english}` has matching `\end{english}`** — same unclosed-environment risk as above.
11. **`\includegraphics` for attention_complexity.png present in at least one chapter** — grep all six chapters for `attention_complexity.png`; if absent, insert the `figure` block into `ch2.tex` (see § Two Mandatory Structural Elements above).
12. **`\begin{table}` model comparison present in at least one chapter** — grep all six chapters for `\begin{table}`; if absent, insert the comparison table into `ch4.tex` (see § Two Mandatory Structural Elements above).

---

## Scope: All 6 Chapters

The BidiAgent validates **all six chapters** (`ch1.tex` through `ch6.tex`), not only Chapter 3. Every chapter may contain English technical terms in Hebrew prose. Chapter 3 receives the additional mandatory-constructs check.

---

## Fix Procedure

When a missing construct is detected:

1. Read the full chapter file content.
2. Identify the exact location where the construct should be inserted (after the first Hebrew paragraph for `\textenglish{}`, at the first formula for `\begin{equation}`, after the first code reference for `\begin{LTR}`).
3. Insert the construct using the minimal text change that does not break surrounding Hebrew paragraph flow.
4. Overwrite the chapter file in-place via `latex_writer_tool` in `write` mode with the corrected full content.
5. Re-run the 10-item validation checklist on the corrected file before proceeding.

---

## BiDi-Correct Paragraph Example

```latex
\chapter{דו-כיווניות בפרסום אקדמי}

מנגנון תשומת הלב של \textenglish{Transformer} מאפשר לכל אסימון ברצף לשים לב
לכל שאר האסימונים. הפונקציה המרכזית היא \textenglish{Scaled Dot-Product Attention}:

\begin{equation}
    \text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
\end{equation}

דוגמה לקוד \textenglish{Python} המממש את החישוב:

\begin{LTR}
\begin{verbatim}
import torch
scores = (Q @ K.transpose(-2, -1)) / math.sqrt(d_k)
attn = torch.softmax(scores, dim=-1) @ V
\end{verbatim}
\end{LTR}
```

---

## Common BiDi Mistake vs. Corrected Form

**Mistake — bare math in RTL context:**
```latex
הנוסחה היא $Q K^T / \sqrt{d_k}$ ומחושבת עבור כל ראש.
```
Problem: bare `$...$` is forbidden in LuaLaTeX BiDi mode and causes undefined behavior.

**Corrected form:**
```latex
הנוסחה היא \(Q K^T / \sqrt{d_k}\) ומחושבת עבור כל ראש.
```
