---
name: matplotlib-tikz
description: Generates complex mathematical graphs and plots using Python's matplotlib library and exports them as high-resolution PNG assets for LaTeX integration; also authors native PGF/TikZ diagrams directly as .tex snippets for inclusion in LuaLaTeX documents. Covers the exact matplotlib script structure for producing an attention complexity comparison plot (O(n²) standard, O(n log n) linear, O(n) recurrent curves) saved at 300 dpi to latex_output/assets/attention_complexity.png, and the complete TikZ skeleton for a scaled dot-product attention data-flow diagram with Q, K, V nodes saved to latex_output/figures/sdp_attention.tex. Enforces import restrictions (only matplotlib.pyplot and numpy allowed), axis labeling conventions, legend requirements, \includegraphics embedding syntax, and arrow-connection patterns for TikZ node graphs.
metadata:
  author: Avi Ayeli
  version: "1.0"
---

# Scientific Figure Generator

## Agent Role

The Scientific Figure Generator produces two artifacts:

1. **`latex_output/assets/attention_complexity.png`** — a matplotlib plot comparing three attention complexity curves.
2. **`latex_output/figures/sdp_attention.tex`** — a TikZ diagram illustrating scaled dot-product attention data flow.

Both are created by the FigureAgent using `python_runner_tool` (for the matplotlib script) and `latex_writer_tool` (for the TikZ snippet).

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
    \includegraphics[width=0.85\textwidth]{latex_output/assets/attention_complexity.png}
    \caption{השוואת מורכבות חישובית: תשומת לב סטנדרטית \textenglish{O(n²)},
             תשומת לב לינארית \textenglish{O(n \log n)}, ורקורנטי \textenglish{O(n)}.}
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

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| PNG is blank | `plt.close(fig)` called before `savefig` | Always `savefig` before `close` |
| TikZ nodes overlap | `node distance` too small | Increase `node distance` or use absolute coordinates |
| Arrow misses node | Wrong anchor name | Use `.north`, `.south`, `.east`, `.west` anchors |
| `! Package tikz Error` | `tikz` not in preamble | Add `\usepackage{tikz}` to `main.tex` |
| `\textenglish` unknown in TikZ | `polyglossia` not loaded | Load order: `fontspec` → `polyglossia` → `tikz` |
| `dpi=300` ignored | Saving as PDF not PNG | Use `.png` extension in `savefig` path |
