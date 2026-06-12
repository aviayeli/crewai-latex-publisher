#!/usr/bin/env python3
"""v2 — patch cover pages: correct Hebrew spelling, ת.ז. ID format, LTR date.

Changes over v1:
  1. Author: 'אבי איילי, ת.ז. [300228160]' (single yod, no \\textenglish ID).
  2. Date: \\textenglish{13.06.2026} — LTR numeric, prevents digit reversal.
  3. Disclaimer text unchanged from v1; \\maketitle override already injected.

Compiles with lualatex → biber → lualatex (3-pass for cross-reference settle).
"""

import os
import subprocess
from pathlib import Path

_LUALATEX = os.environ.get("LUALATEX_BIN", "lualatex")
_BIBER = os.environ.get("BIBER_BIN", "biber")

RESULTS = Path("results")
ARTICLES = [
    "1_sine_wave",
    "2_security",
    "3_xlstm",
    "4_orchestration",
]

_SENTINEL_V1 = "% RTL-COVER-PATCH-APPLIED"
_SENTINEL_V2 = "% COVER-PATCH-V2"
_SENTINEL_V3 = "% COVER-PATCH-V3"

# Exact author name+ID required by the course rubric.
# \textenglish{} prevents BiDi digit-stacking inside the RTL author block.
_AUTHOR_NEW = r"אבי איילי, ת.ז. [\textenglish{300228160}]"

# All historical author+ID forms we may encounter in results/ main.tex files.
_OLD_AUTHORS = [
    r"אבי איילי, ת.ז. [300228160]",             # v2-patched (no textenglish)
    r"אבי אייאלי --- \textenglish{300228160}",   # v1-patched (double yod)
    r"Avi Ayeli --- \textenglish{300228160}",     # pre-v1 (English name)
]

_DATE_OLD = r"\date{\today}"
_DATE_NEW = r"\date{\textenglish{13.06.2026}}"

# Raw-string LaTeX block for first-time application (no v1 sentinel present).
_LATEX_BLOCK = r"""% RTL-safe title page with mandatory GenAI disclaimer.
% report.cls wraps \@author in \begin{tabular}{c} (LTR box) — that
% visually reverses Hebrew text. This override uses \begin{RTL} instead.
\makeatletter
\renewcommand{\maketitle}{%
  \begin{titlepage}%
    \begin{RTL}%
      \null\vfill%
      \begin{center}%
        {\LARGE\bfseries\@title\par}%
        \vspace{2em}%
        {\large\@author\par}%
        \vspace{1em}%
        {\large\@date\par}%
        \vspace{3em}%
        {\small\itshape
          המאמר נוצר בסיוע כלי \textenglish{Gen AI},
          כנדרש בהנחיות הקורס.\par}%
      \end{center}%
      \vfill\null%
    \end{RTL}%
  \end{titlepage}%
  \setcounter{footnote}{0}%
}
\makeatother
"""


def _patch_main_tex(path: Path) -> bool:
    """Patch main.tex in-place. Return True if the file was modified."""
    text = path.read_text(encoding="utf-8")
    if _SENTINEL_V3 in text:
        print(f"  [SKIP] {path.parent.name}: v3 patch already applied")
        return False

    # Ensure \maketitle override is present (inject before \begin{document}
    # only if v1 was never applied to this file).
    if _SENTINEL_V1 not in text:
        v1_block = _SENTINEL_V1 + "\n" + _LATEX_BLOCK
        text = text.replace("\\begin{document}", v1_block + "\\begin{document}")

    # Fix author name+ID — replace all known historical forms.
    for old in _OLD_AUTHORS:
        text = text.replace(old, _AUTHOR_NEW)

    # Fix date: wrap in \textenglish for LTR numeric rendering.
    text = text.replace(_DATE_OLD, _DATE_NEW)

    # Mark v3 complete, adjacent to the highest existing sentinel.
    for sentinel in (_SENTINEL_V2, _SENTINEL_V1):
        if sentinel in text:
            text = text.replace(sentinel, sentinel + "\n" + _SENTINEL_V3, 1)
            break
    else:
        text = _SENTINEL_V3 + "\n" + text

    path.write_text(text, encoding="utf-8")
    return True


def _compile(base: Path) -> None:
    """Run lualatex → biber → lualatex (3-pass)."""
    lualatex = [_LUALATEX, "-interaction=nonstopmode", "main.tex"]
    for cmd in [lualatex, [_BIBER, "main"], lualatex]:
        subprocess.run(cmd, cwd=base, check=True)


def fix_article(name: str) -> None:
    base = RESULTS / name
    main_tex = base / "main.tex"
    if not main_tex.exists():
        print(f"[ERROR] {name}: results/main.tex not found — skipping")
        return
    if _patch_main_tex(main_tex):
        print(f"[CHECKPOINT] {name}: main.tex patched. Compiling...")
        _compile(base)
        print(f"[CHECKPOINT] {name}: PDF regenerated → {base}/main.pdf")


if __name__ == "__main__":
    for article in ARTICLES:
        fix_article(article)
