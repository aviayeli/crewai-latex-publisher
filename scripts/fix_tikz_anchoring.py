"""
Fix two TikZ layout bugs on document page 12 (sdp_attention.tex):

1. RTL mirroring — the tikzpicture inherits Polyglossia's global RTL paragraph
   direction, inverting the x-axis (TikZ x=5 renders at the LEFT, x=0 at the RIGHT).
   Fix: wrap the entire tikzpicture in \\begin{LTR}...\\end{LTR}.

2. Node overlap — original `operation` circles used node distance=1.5cm (42pt)
   with minimum size=1.6cm (45pt), so adjacent circles overlap by 3pt.
   Fix: replace all per-style circle nodes with a single `every node/.style` using
   rectangular nodes, anchor=center, and 1.8cm vertical spacing (gap > node height).

The canonical replacement follows the template in skills/matplotlib-tikz/SKILL.md,
which uses anchor=center globally and ensures LTR rendering via \\begin{LTR}.
"""

import sys
from pathlib import Path

OUTPUT_DIR = Path("latex_output")
DRY_RUN = "--dry-run" in sys.argv

CANONICAL_TIKZ = r"""% Scaled Dot-Product Attention — LTR-safe anchored canonical
% \begin{LTR}: prevents RTL mirror; anchor=center: text on shape.
\begin{LTR}
\begin{tikzpicture}[
    every node/.style={
        draw,
        rounded corners=3pt,
        minimum width=2.2cm,
        minimum height=0.8cm,
        align=center,
        anchor=center,
        font=\small
    },
    arrow/.style={->, >=stealth, thick}
]

% Input nodes — bottom row
\node (Q)       at (0,   0) {Q};
\node (K)       at (2.5, 0) {K};
\node (V)       at (5,   0) {V};

% Computation chain (left branch, 1.8 cm vertical spacing > 0.8 cm node height)
\node (matmul1) at (1.25, 1.8) {MatMul};
\node (scale)   at (1.25, 3.6) {Scale \\ \(\div\sqrt{d_k}\)};
\node (softmax) at (1.25, 5.4) {Softmax};

% Merge + output
\node           (matmul2) at (3.0, 7.2) {MatMul};
\node[fill=gray!20] (output)  at (3.0, 9.0) {Output};

% Q and K feed into first MatMul
\draw[arrow] (Q.north) -- ++(0,0.5) -| (matmul1.south west);
\draw[arrow] (K.north) -- ++(0,0.5) -| (matmul1.south east);

% Vertical computation chain
\draw[arrow] (matmul1.north) -- (scale.south);
\draw[arrow] (scale.north)   -- (softmax.south);

% Softmax and V feed into second MatMul
\draw[arrow] (softmax.north) -- ++(0,0.5) -| (matmul2.south west);
\draw[arrow] (V.north)       -- ++(0,6.5) -| (matmul2.south east);

% Final output
\draw[arrow] (matmul2.north) -- (output.south);

\end{tikzpicture}
\end{LTR}
"""


def fix_sdp_attention(path: Path) -> int:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if current.strip() == CANONICAL_TIKZ.strip():
        print(f"  [SKIP] {path}: already canonical")
        return 0
    if not DRY_RUN:
        path.write_text(CANONICAL_TIKZ, encoding="utf-8")
    has_ltr = r"\begin{LTR}" in current
    has_anchor = "anchor=center" in current
    reasons = []
    if not has_ltr:
        reasons.append("added \\begin{LTR} wrapper (RTL-mirror fix)")
    if not has_anchor:
        reasons.append("added anchor=center to every node/.style")
    reasons.append("replaced circle nodes with rectangular nodes (no overlap)")
    print(f"  [FIX]  {path}: {'; '.join(reasons)}")
    return 1


def main() -> None:
    tikz = OUTPUT_DIR / "figures" / "sdp_attention.tex"
    if not tikz.exists():
        print(f"  [WARN] {tikz} not found — cannot fix")
        return

    fixes = fix_sdp_attention(tikz)
    print(f"\n[CHECKPOINT] fix_tikz_anchoring.py done: {fixes} file(s) patched.")
    if fixes == 0:
        print("  Nothing changed — file already matches canonical version.")


if __name__ == "__main__":
    main()
