#!/usr/bin/env python3
"""Patch cover pages in results/ for BiDi, Hebrew author, and AI disclaimer.

Retroactive fix for three regressions on mass-produced article cover pages:
  1. Author name rendered in English instead of Hebrew.
  2. Hebrew title-page text visually reversed (report.cls wraps \\author
     in \\begin{tabular}{c} — a LTR box — reversing RTL Hebrew text).
  3. Mandatory Gen AI usage disclaimer absent from the title page.

Patches each results/{article}/main.tex then runs two lualatex passes to
regenerate the PDF (biber is skipped — bib data unchanged, .bbl reused).
"""

import os
import subprocess
from pathlib import Path

_LUALATEX = os.environ.get("LUALATEX_BIN", "lualatex")

RESULTS = Path("results")
ARTICLES = [
    "1_sine_wave",
    "2_security",
    "3_xlstm",
    "4_orchestration",
]

AUTHOR_EN = "Avi Ayeli"
AUTHOR_HE = "אבי אייאלי"

# Sentinel prevents the patch from being applied twice (idempotency).
_SENTINEL = "% RTL-COVER-PATCH-APPLIED"

# Raw string: no f-string interpolation, so LaTeX {braces} are literal.
_LATEX_BLOCK = r"""% RTL-safe title page with mandatory GenAI disclaimer.
% report.cls default wraps \@author in \begin{tabular}{c} — a LTR box —
% which visually reverses Hebrew author text. This override avoids that.
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

_PATCH = _SENTINEL + "\n" + _LATEX_BLOCK


def _patch_main_tex(path: Path) -> bool:
    """Patch main.tex in-place. Return True if the file was modified."""
    text = path.read_text(encoding="utf-8")
    if _SENTINEL in text:
        print(f"  [SKIP] {path.parent.name}: patch already applied")
        return False
    text = text.replace(AUTHOR_EN, AUTHOR_HE)
    text = text.replace("\\begin{document}", _PATCH + "\\begin{document}")
    path.write_text(text, encoding="utf-8")
    return True


def _compile(base: Path) -> None:
    """Run two lualatex passes (bib unchanged — reuse existing .bbl)."""
    cmd = [_LUALATEX, "-interaction=nonstopmode", "main.tex"]
    for _ in range(2):
        subprocess.run(cmd, cwd=base, check=True)


def fix_article(name: str) -> None:
    base = RESULTS / name
    main_tex = base / "main.tex"
    if not main_tex.exists():
        print(f"[ERROR] {name}: results/main.tex not found — skipping")
        return
    modified = _patch_main_tex(main_tex)
    if not modified:
        return
    print(f"[CHECKPOINT] {name}: main.tex patched. Compiling...")
    _compile(base)
    print(f"[CHECKPOINT] {name}: PDF regenerated → {base}/main.pdf")


if __name__ == "__main__":
    for article in ARTICLES:
        fix_article(article)
