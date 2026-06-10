"""
Fix two layout-overflow bugs found in generated .tex files:

1. sdp_attention.tex — operation circle nodes have text width=0.8cm which is too
   narrow for labels like "Softmax" (43pt rendered), causing text to visually overflow
   the circle boundary. Fix: widen to 1.5cm and add minimum size=1.6cm.

2. ch4.tex — model comparison table uses `c` (no-wrap) for the Notes column.
   Long phrases like "bidirectional context" and "temporal modeling" overflow the
   right page margin (detected at x>524pt on A4 with 2.5cm margins). Fix: change
   the last column to p{4cm} so text wraps.
"""

import sys
from pathlib import Path

OUTPUT_DIR = Path("latex_output")
DRY_RUN = "--dry-run" in sys.argv


def fix_tikz_circles(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    old = (
        "        text width=0.8cm,\n"
        "        text centered,\n"
        "        font=\\small\\bfseries"
    )
    new = (
        "        text width=1.5cm,\n"
        "        minimum size=1.6cm,\n"
        "        align=center,\n"
        "        font=\\small\\bfseries"
    )
    if old not in text:
        print(f"  [SKIP] {path}: operation-circle pattern not found (already fixed?)")
        return 0
    patched = text.replace(old, new, 1)
    if not DRY_RUN:
        path.write_text(patched, encoding="utf-8")
    print(f"  [FIX]  {path}: widened operation circles "
          "(text width 0.8→1.5cm, added minimum size=1.6cm)")
    return 1


def fix_table_column(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    old = r"\begin{tabular}{|l|c|c|c|}"
    new = r"\begin{tabular}{|l|c|c|p{4cm}|}"
    if old not in text:
        print(f"  [SKIP] {path}: 4-column tabular pattern not found (already fixed?)")
        return 0
    patched = text.replace(old, new, 1)
    if not DRY_RUN:
        path.write_text(patched, encoding="utf-8")
    print(f"  [FIX]  {path}: changed Notes column from `c` to `p{{4cm}}`")
    return 1


def main() -> None:
    fixes = 0

    tikz = OUTPUT_DIR / "figures" / "sdp_attention.tex"
    if tikz.exists():
        fixes += fix_tikz_circles(tikz)
    else:
        print(f"  [WARN] {tikz} not found — skipping circle fix")

    ch4 = OUTPUT_DIR / "chapters" / "ch4.tex"
    if ch4.exists():
        fixes += fix_table_column(ch4)
    else:
        print(f"  [WARN] {ch4} not found — skipping table fix")

    print(f"\n[CHECKPOINT] fix_figure_overflow.py done: {fixes} file(s) patched.")
    if fixes == 0:
        print("  Nothing changed — patterns may have already been corrected.")


if __name__ == "__main__":
    main()
