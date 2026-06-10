---
name: matplotlib-tikz
description: Generates complex mathematical graphs and plots using Python's matplotlib library and exports them as high-resolution PNG assets for LaTeX integration; also authors native PGF/TikZ diagrams directly as .tex snippets for inclusion in LuaLaTeX documents. Covers the exact matplotlib script structure for producing an attention complexity comparison plot (O(n²) standard, O(n log n) linear, O(n) recurrent curves) saved at 300 dpi to latex_output/assets/attention_complexity.png, and the complete TikZ skeleton for a scaled dot-product attention data-flow diagram with Q, K, V nodes saved to latex_output/figures/sdp_attention.tex. Enforces import restrictions (only matplotlib.pyplot and numpy allowed), axis labeling conventions, legend requirements, \includegraphics embedding syntax, and arrow-connection patterns for TikZ node graphs.
metadata:
  author: Avi Ayeli
  version: "1.0"
---

# Scientific Figure Generator

## Agent Role

The Scientific Figure Generator produces two artifacts **and embeds them into the chapter files**:

1. **`latex_output/assets/attention_complexity.png`** — a matplotlib plot comparing three attention complexity curves.
2. **`latex_output/figures/sdp_attention.tex`** — a TikZ diagram illustrating scaled dot-product attention data flow.

Both are created by the FigureAgent using `python_runner_tool` (for the matplotlib script) and `latex_writer_tool` (for the TikZ snippet).

---

## CRITICAL: Figures MUST Be Embedded in Chapters — Never Left as Orphaned Files

Generating a PNG or TikZ file without embedding it in a chapter `.tex` file is a **contract violation**. The PDF evaluator checks the rendered output, not the file system. A figure that exists in `assets/` or `figures/` but is not referenced by any `\includegraphics` or `\input{}` command will be **invisible in the PDF and will score zero**.

### Step A — Embed the PNG graph into `ch2.tex`

Immediately after `python_runner_tool` confirms the PNG was saved, use `latex_writer_tool` in `append` mode to add the figure block to `latex_output/chapters/ch2.tex`:

```latex

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.85\textwidth]{../assets/attention_complexity.png}
    \caption{השוואת מורכבות חישובית: תשומת לב סטנדרטית \textenglish{$O(n^{2})$},
             תשומת לב לינארית \textenglish{$O(n \log n)$}, ורקורנטי \textenglish{$O(n)$}.}
    \label{fig:attention_complexity}
\end{figure}
```

**Path note:** from inside `latex_output/chapters/ch2.tex`, the assets directory is at `../assets/`. Always use this relative path, not the absolute `latex_output/assets/` path.

### Step B — Embed the TikZ diagram into `ch3.tex`

Immediately after `latex_writer_tool` confirms `sdp_attention.tex` was written, use `latex_writer_tool` in `append` mode to add the input block to `latex_output/chapters/ch3.tex`:

```latex

\begin{figure}[htbp]
    \centering
    \begin{tikzpicture}[
        node distance=1.2cm and 1.5cm,
        every node/.style={draw, rounded corners, minimum width=2.2cm, minimum height=0.7cm,
                           align=center, font=\small},
        arrow/.style={->, >=stealth, thick}
    ]
    \node (Q) at (0, 0)   {\textenglish{Q}};
    \node (K) at (2.5, 0) {\textenglish{K}};
    \node (V) at (5, 0)   {\textenglish{V}};
    \node (matmul1) at (1.25, 1.6) {\textenglish{MatMul}};
    \node (scale)   at (1.25, 3.2) {\textenglish{Scale} \\ \(\div \sqrt{d_k}\)};
    \node (softmax) at (1.25, 4.8) {\textenglish{Softmax}};
    \node (matmul2) at (3.0, 6.4)  {\textenglish{MatMul}};
    \node[fill=gray!20] (output) at (3.0, 8.0) {\textenglish{Output}};
    \draw[arrow] (Q.north) -- ++(0,0.5) -| (matmul1.south west);
    \draw[arrow] (K.north) -- ++(0,0.5) -| (matmul1.south east);
    \draw[arrow] (matmul1.north) -- (scale.south);
    \draw[arrow] (scale.north) -- (softmax.south);
    \draw[arrow] (softmax.north) -- ++(0,0.5) -| (matmul2.south west);
    \draw[arrow] (V.north) -- ++(0,5.9) -| (matmul2.south east);
    \draw[arrow] (matmul2.north) -- (output.south);
    \end{tikzpicture}
    \caption{ארכיטקטורת \textenglish{Scaled Dot-Product Attention}: זרימת הנתונים מ-\textenglish{Q}, \textenglish{K}, \textenglish{V} לפלט.}
    \label{fig:sdp_attention}
\end{figure}
```

### Checkpoint Protocol (MANDATORY)

After each embedding step, emit a checkpoint:
- `[CHECKPOINT] PNG embedded in ch2.tex — \includegraphics present.`
- `[CHECKPOINT] TikZ embedded in ch3.tex — \begin{tikzpicture} present.`

If either chapter file does not exist yet (was not written by ContentAgent), create a minimal skeleton with `latex_writer_tool` in `write` mode:

```
path='latex_output/chapters/ch2.tex', mode='write', content='\chapter{רקע תיאורטי}\n'
```

Then immediately append the figure block.

---

---

## Artifact 1: Attention Complexity PNG

### Output Path

```
latex_output/assets/attention_complexity.png
```

This path is exact and must not be changed. The `\includegraphics` command in `main.tex` references this path.

### Three Required Curves

The plot must display exactly three curves over a shared x-axis (sequence length `n`):

| Curve | Label | Complexity | Color |
|-------|-------|------------|-------|
| Standard self-attention | "Standard Attention O(n²)" | `n**2` | `#e74c3c` (red) |
| Linear attention | "Linear Attention O(n log n)" | `n * np.log2(n)` | `#2ecc71` (green) |
| Recurrent model | "Recurrent O(n)" | `n` | `#3498db` (blue) |

### Axis Labels

- **x-axis:** `"Sequence Length (n)"`
- **y-axis:** `"Complexity"`
- **Legend:** required; use `plt.legend()` with `loc="upper left"`.

### Saving at 300 dpi

```python
plt.savefig(path, dpi=300, bbox_inches='tight')
```

`bbox_inches='tight'` prevents axis labels from being clipped at the figure boundary.

### Import Restriction

The matplotlib script may only import from `matplotlib.pyplot` and `numpy`. No other imports (`os`, `pathlib`, `subprocess`, `requests`, etc.) are permitted — the `python_runner_tool` AST scanner will reject any additional import.

```python
import matplotlib.pyplot as plt
import numpy as np
```

### Complete Matplotlib Script

```python
import matplotlib.pyplot as plt
import numpy as np

# --- Data ---
n = np.linspace(1, 512, 512)

standard = n ** 2
linear = n * np.log2(n)
recurrent = n

# --- Plot ---
fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(n, standard, color="#e74c3c", linewidth=2, label="Standard Attention O(n²)")
ax.plot(n, linear,   color="#2ecc71", linewidth=2, label="Linear Attention O(n log n)")
ax.plot(n, recurrent, color="#3498db", linewidth=2, label="Recurrent O(n)")

# --- Labels and legend ---
ax.set_xlabel("Sequence Length (n)", fontsize=12)
ax.set_ylabel("Complexity", fontsize=12)
ax.legend(loc="upper left", fontsize=10)
ax.grid(True, linestyle="--", alpha=0.4)

# --- Save ---
plt.savefig("latex_output/assets/attention_complexity.png", dpi=300, bbox_inches="tight")
plt.close(fig)
```

---

## Embedding the PNG in LaTeX

Use a `figure` environment with `\includegraphics` in the chapter that references the plot:

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.85\textwidth]{../assets/attention_complexity.png}
    \caption{השוואת מורכבות חישובית: תשומת לב סטנדרטית \textenglish{$O(n^{2})$},
             תשומת לב לינארית \textenglish{$O(n \log n)$}, ורקורנטי \textenglish{$O(n)$}.}
    \label{fig:attention_complexity}
\end{figure}
```

- `width=0.85\textwidth` scales the image to 85% of the text column width.
- `label` must be unique within the document; use it for `\ref{fig:attention_complexity}`.
- The `graphicx` package must be loaded in `main.tex` preamble (it is in the required package list).

---

## Artifact 2: Scaled Dot-Product Attention TikZ Diagram

### Output Path

```
latex_output/figures/sdp_attention.tex
```

This file is a TikZ fragment (no `\documentclass`, no `\begin{document}`). It is included in a chapter via `\input{latex_output/figures/sdp_attention.tex}`.

### Node Layout

The diagram represents the data flow: **Q**, **K**, **V** inputs → **MatMul (QKᵀ)** → **Scale (÷√d_k)** → **Softmax** → **MatMul with V** → **Output**.

Nodes are arranged vertically (bottom input, top output).

### Connecting Nodes with Arrows

Use TikZ `\draw[->]` with named node anchors. Each `\node` has a label and an explicit name for wiring:

```latex
\draw[->] (Q.north) -- (matmul1.south west);
\draw[->] (K.north) -- (matmul1.south east);
```

### Complete TikZ Skeleton for `sdp_attention.tex`

```latex
\begin{tikzpicture}[
    node distance=1.2cm and 1.5cm,
    every node/.style={draw, rounded corners, minimum width=2.2cm, minimum height=0.7cm,
                       align=center, font=\small},
    arrow/.style={->, >=stealth, thick}
]

% Input nodes
\node (Q) at (0, 0)   {\textenglish{Q}};
\node (K) at (2.5, 0) {\textenglish{K}};
\node (V) at (5, 0)   {\textenglish{V}};

% MatMul QK^T
\node (matmul1) at (1.25, 1.6) {\textenglish{MatMul} \\ \textenglish{(QK\textsuperscript{T})}};

% Scale
\node (scale) at (1.25, 3.2) {\textenglish{Scale} \\ \(\div \sqrt{d_k}\)};

% Softmax
\node (softmax) at (1.25, 4.8) {\textenglish{Softmax}};

% MatMul with V
\node (matmul2) at (3.0, 6.4) {\textenglish{MatMul}};

% Output
\node[fill=gray!20] (output) at (3.0, 8.0) {\textenglish{Output}};

% Arrows: Q, K -> matmul1
\draw[arrow] (Q.north) -- ++(0, 0.5) -| (matmul1.south west);
\draw[arrow] (K.north) -- ++(0, 0.5) -| (matmul1.south east);

% matmul1 -> scale -> softmax
\draw[arrow] (matmul1.north) -- (scale.south);
\draw[arrow] (scale.north)   -- (softmax.south);

% softmax, V -> matmul2
\draw[arrow] (softmax.north) -- ++(0, 0.5) -| (matmul2.south west);
\draw[arrow] (V.north)       -- ++(0, 5.9) -| (matmul2.south east);

% matmul2 -> output
\draw[arrow] (matmul2.north) -- (output.south);

\end{tikzpicture}
```

### Including the TikZ Diagram in a Chapter

```latex
\begin{figure}[htbp]
    \centering
    \input{latex_output/figures/sdp_attention.tex}
    \caption{תרשים \textenglish{Scaled Dot-Product Attention} עם צמתי
             \textenglish{Q}, \textenglish{K}, \textenglish{V}.}
    \label{fig:sdp_attention}
\end{figure}
```

The `tikz` package must be loaded in `main.tex` preamble (it is in the required package list).

---

## CRITICAL: Text Wrapping in Figures — Mandatory Node and Table Constraints

**Root cause:** TikZ `\node` shapes do not auto-wrap text by default. Without an explicit
`text width` constraint, a node expands horizontally to fit the entire label on one line,
overflowing the drawn shape (circle or rectangle) and potentially colliding with adjacent
nodes. Table columns declared as `c` (centered) similarly do not wrap — they expand
indefinitely and push content outside the page margins.

### Rule TW-1 — Every TikZ `\node` with descriptive text MUST have `text width` + `align`

```latex
% FORBIDDEN — text overflows the circle at runtime
\node[circle, text width=0.8cm] (op) {...Softmax...};

% CORRECT — text wraps inside the shape; minimum size keeps shape visible
\node[circle, text width=1.5cm, minimum size=1.6cm, align=center] (op) {...Softmax...};
```

**Minimum `text width` guide by node style:**

| Style | Shape | Recommended `text width` | Add `minimum size`? |
|-------|-------|--------------------------|---------------------|
| Operation (circle) | circle | ≥ 1.5cm | Yes — match text width |
| Block (rectangle) | rectangle | ≥ 1.8cm | No |
| Input/output | rectangle | ≥ 1.5cm | No |
| Annotation text box | plain | 4–6cm | No |

Always set `align=center` (or `align=left` for prose) on every node that contains more
than a single character. Never rely on `text centered` alone — it does not constrain width.

### Rule TW-2 — Table columns with prose MUST use `p{Xcm}` not `c`

The `c` column type does not wrap. Any column that contains English phrases longer than
a few words must use `p{Xcm}` (paragraph column):

```latex
% FORBIDDEN — Notes column expands, overflows right page margin
\begin{tabular}{|l|c|c|c|}

% CORRECT — Notes column wraps at 4 cm
\begin{tabular}{|l|c|c|p{4cm}|}
```

Choose `p{4cm}` for a 4-column table on A4 with 2.5 cm margins. Adjust down if the
other columns are wide. Always verify with `pdfinfo` or PyMuPDF that no word appears
right of x=524 pt (the right text-area boundary on A4).

---

## CRITICAL: TW-3 — Node Anchoring, Positioning, and RTL-Safe Embedding

### Rule TW-3a — Every `\node` must declare `anchor=center` explicitly

In TikZ, nodes placed with `at (x,y)` use the center by default, but this default is
fragile: any `every node/.style` override or inherited style can silently shift the
anchor. Always declare it explicitly so text sits exactly on its intended target:

```latex
% FORBIDDEN — anchor implicit, fragile under style inheritance
\node[draw] (foo) at (2.5, 3) {text};

% CORRECT — anchor declared, predictable placement
\node[draw, anchor=center] (foo) at (2.5, 3) {text};

% CORRECT — set globally for all nodes
every node/.style={draw, align=center, anchor=center, ...}
```

For **edge labels** (text on an arrow), use `midway` with a direction:
```latex
\draw[arrow] (A) -- node[midway, above, anchor=center] {label} (B);
```

### Rule TW-3b — TikZ figures MUST be wrapped in `\begin{LTR}...\end{LTR}`

**Root cause of RTL mirroring:** When Polyglossia sets Hebrew as the main document
language, the entire document runs in RTL mode. A TikZ picture inherits this RTL
paragraph direction, causing its x-axis to run right-to-left. A node at TikZ x=5
therefore renders on the LEFT side of the page while x=0 renders on the RIGHT — the
diagram is a mirror image of the intended layout.

**Fix:** Wrap every `\begin{tikzpicture}` in `\begin{LTR}...\end{LTR}` (provided by
the bidi package that polyglossia auto-loads for RTL documents):

```latex
% FORBIDDEN — tikzpicture in inherited RTL context; x-axis is mirrored
\begin{figure}[htbp]
    \centering
    \begin{tikzpicture}[...]
    ...
    \end{tikzpicture}
```

```latex
% CORRECT — LTR wrapper restores standard left-to-right x-axis
\begin{figure}[htbp]
    \centering
    \begin{LTR}
    \begin{tikzpicture}[...]
    ...
    \end{tikzpicture}
    \end{LTR}
```

This applies to **any** TikZ content embedded in documents with `\setmainlanguage{hebrew}`.
The `sdp_attention.tex` fragment must begin with `\begin{LTR}` and end with `\end{LTR}`.

### Rule TW-3c — Node spacing must exceed node diameter

When using `minimum size` on circle nodes, adjacent nodes will **visually overlap** if
`node distance ≤ minimum size`. Always ensure:

```
node_distance > maximum(minimum_size, rendered_text_width + padding)
```

Prefer rectangular nodes (`draw, rounded corners`) over circles for multi-word labels
to avoid this constraint — rectangles grow vertically with text, circles do not.

---

## CRITICAL: Math Mode Is Mandatory in All Captions and TikZ Labels

Any mathematical expression inside a `\caption{}` or a TikZ `\node{...}` label
**MUST** be wrapped in inline math mode (`$...$` or `\(...\)`).

**Root cause:** LaTeX math operators (`\log`, `\sin`, `\sqrt`, `\sum`, etc.) are only
defined inside math mode. Writing `\textenglish{O(n \log n)}` without `$...$` inside
the `\textenglish{}` argument produces `! Missing $ inserted` and aborts compilation.
The RTL BiDi algorithm also reverses bare notation — `n^2` renders as `2^n` in Hebrew
paragraphs unless protected by math mode.

### Mandatory pattern for Big-O complexity in captions

```latex
% FORBIDDEN — \log outside math mode causes compilation failure
\caption{... \textenglish{O(n \log n)} ...}
\caption{... \textenglish{O(n\textsuperscript{2})} ...}

% CORRECT — math mode wraps all notation including operators
\caption{... \textenglish{$O(n \log n)$} ...}
\caption{... \textenglish{$O(n^{2})$} ...}
\caption{... \textenglish{$O(n)$} ...}
```

### General rule for all captions and TikZ labels

| Expression type | Wrong | Correct |
|-----------------|-------|---------|
| Big-O with operator | `\textenglish{O(n \log n)}` | `\textenglish{$O(n \log n)$}` |
| Superscript | `\textenglish{O(n\textsuperscript{2})}` | `\textenglish{$O(n^{2})$}` |
| Fraction in node | `\node{d_k / \sqrt{d}}` | `\node{$d_k / \sqrt{d}$}` |
| Subscript | `\textenglish{W_hh}` | `\textenglish{$W_{hh}$}` |
| Any `\log`, `\sin`, `\tanh`, etc. | `\textenglish{\log n}` | `\textenglish{$\log n$}` |

Apply this rule **before calling `latex_writer_tool`** — do not rely on the BiDi agent
to catch caption errors post-hoc.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| PNG is blank | `plt.close(fig)` called before `savefig` | Always `savefig` before `close` |
| TikZ nodes overlap | `node distance` too small | Increase `node distance` or use absolute coordinates |
| Arrow misses node | Wrong anchor name | Use `.north`, `.south`, `.east`, `.west` anchors |
| `! Package tikz Error` | `tikz` not in preamble | Add `\usepackage{tikz}` to `main.tex` |
| `\textenglish` unknown in TikZ | `polyglossia` not loaded | Load order: `fontspec` → `polyglossia` → `tikz` |
| `dpi=300` ignored | Saving as PDF not PNG | Use `.png` extension in `savefig` path |
