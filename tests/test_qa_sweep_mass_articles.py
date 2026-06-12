"""QA sweep for the 4 mass-produced articles in results/.

Rubric checks (report-only — no fixes applied):
  1. Page count >= 15
  2. Headers (left-aligned chapter name) and Footers (centred page number)
  3. BiDi integrity: page numbers must be decimal digits only (no reversed RTL)
  4. Required elements: Tables, Math formulas, Python-generated graphs (images)
  5. Data-chained citations: \\cite{} keys must all be present in refs.bib
  6. Visual anomalies: Overfull/Underfull hboxes from LaTeX log
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

import fitz  # PyMuPDF
import pytest

# ---------------------------------------------------------------------------
RESULTS_ROOT = Path(__file__).parent.parent / "results"
ARTICLES = {
    "1_sine_wave": RESULTS_ROOT / "1_sine_wave",
    "2_security": RESULTS_ROOT / "2_security",
    "3_xlstm": RESULTS_ROOT / "3_xlstm",
    "4_orchestration": RESULTS_ROOT / "4_orchestration",
}
MIN_PAGES = 15


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class ArticleData(NamedTuple):
    name: str
    pdf: fitz.Document
    main_tex: str
    chapters_tex: dict[str, str]  # filename -> content
    refs_bib: str
    latex_log: str


def load_article(name: str, root: Path) -> ArticleData:
    pdf = fitz.open(root / "main.pdf")
    main_tex = (root / "main.tex").read_text(encoding="utf-8")
    chapters = {}
    for ch in sorted((root / "chapters").glob("*.tex")):
        chapters[ch.name] = ch.read_text(encoding="utf-8")
    bib = root / "refs.bib"
    refs = bib.read_text(encoding="utf-8") if bib.exists() else ""
    log_path = root / "main.log"
    log = (
        log_path.read_text(encoding="utf-8", errors="replace")
        if log_path.exists()
        else ""
    )
    return ArticleData(name, pdf, main_tex, chapters, refs, log)


def _all_chapter_text(data: ArticleData) -> str:
    return "\n".join(data.chapters_tex.values())


def _bib_keys(data: ArticleData) -> set[str]:
    return set(re.findall(r"@\w+\{([^,]+),", data.refs_bib))


def _cite_keys(data: ArticleData) -> set[str]:
    raw = re.findall(r"\\cite\{([^}]+)\}", _all_chapter_text(data))
    keys: set[str] = set()
    for group in raw:
        for k in group.split(","):
            keys.add(k.strip())
    return keys


def _pdf_page_texts(data: ArticleData) -> list[str]:
    return [page.get_text() for page in data.pdf]


# ---------------------------------------------------------------------------
# Parametrised fixture
# ---------------------------------------------------------------------------

@pytest.fixture(params=list(ARTICLES.keys()))
def article(request) -> ArticleData:
    name = request.param
    return load_article(name, ARTICLES[name])


# ---------------------------------------------------------------------------
# 1. Page count
# ---------------------------------------------------------------------------

def test_minimum_page_count(article: ArticleData) -> None:
    """PDF must be at least 15 pages."""
    actual = len(article.pdf)
    assert actual >= MIN_PAGES, (
        f"[{article.name}] Only {actual} pages — minimum is {MIN_PAGES}"
    )


# ---------------------------------------------------------------------------
# 2. Headers and Footers
# ---------------------------------------------------------------------------

def test_headers_present(article: ArticleData) -> None:
    """At least one non-title page should carry a non-empty header (chapter mark)."""
    pages_with_header = 0
    for page in article.pdf:
        blocks = page.get_text("blocks")
        # fancyhdr places running head in the topmost region (y < 80 pts)
        for _x0, y0, _x1, _y1, text, *_ in blocks:
            if y0 < 80 and text.strip():
                pages_with_header += 1
                break
    # Allow cover/TOC to lack a header; require at least half the content pages
    content_pages = max(1, len(article.pdf) - 2)
    assert pages_with_header >= content_pages * 0.5, (
        f"[{article.name}] Headers found on only {pages_with_header} pages "
        f"(expected ≥ {content_pages * 0.5:.0f} of {content_pages} content pages)"
    )


def test_footers_present(article: ArticleData) -> None:
    """Every page (except perhaps the very first) should have a page-number footer."""
    pages = list(article.pdf)
    height = pages[0].rect.height
    pages_with_footer = 0
    for page in pages:
        blocks = page.get_text("blocks")
        for _x0, _y0, _x1, y1, text, *_ in blocks:
            # Footer region: bottom 60 pts
            if y1 > height - 60 and re.search(r"\d+", text):
                pages_with_footer += 1
                break
    # Allow up to 1 page without a footer (blank pages etc.)
    assert pages_with_footer >= len(pages) - 1, (
        f"[{article.name}] Footer missing on {len(pages) - pages_with_footer} pages"
    )


def test_plain_pagestyle_override_in_preamble(article: ArticleData) -> None:
    """\\fancypagestyle{{plain}} override must be defined in main.tex."""
    assert "fancypagestyle{plain}" in article.main_tex, (
        f"[{article.name}] Missing \\fancypagestyle{{plain}} override — "
        "chapter-opening pages will show default plain style (no footer)"
    )


# ---------------------------------------------------------------------------
# 3. BiDi Integrity
# ---------------------------------------------------------------------------

def test_thepage_wrapped_in_textenglish(article: ArticleData) -> None:
    r"""\\thepage must be redefined to \textenglish{\arabic{page}} for LTR digits."""
    needle = r"\renewcommand{\thepage}{\textenglish{\arabic{page}}}"
    assert needle in article.main_tex, (
        f"[{article.name}] \\thepage not wrapped in \\textenglish — "
        "page numbers may render in reversed RTL order"
    )


def test_page_numbers_are_decimal(article: ArticleData) -> None:
    """Every footer page-number token extracted by PyMuPDF must be a plain integer."""
    pages = list(article.pdf)
    height = pages[0].rect.height
    bad_pages: list[int] = []
    for i, page in enumerate(pages, start=1):
        for _x0, _y0, _x1, y1, text, *_ in page.get_text("blocks"):
            if y1 > height - 60:
                stripped = text.strip()
                # Must be only digits (possibly surrounded by whitespace)
                if stripped and not re.fullmatch(r"\d+", stripped):
                    # Ignore multi-word footer lines that happen to contain a digit
                    tokens = stripped.split()
                    page_token = tokens[-1] if tokens else ""
                    if page_token and not re.fullmatch(r"\d+", page_token):
                        bad_pages.append(i)
    assert not bad_pages, (
        f"[{article.name}] Non-decimal page number tokens on PDF pages: {bad_pages}"
    )


def test_section_numbers_use_textenglish(article: ArticleData) -> None:
    r"""\\thesection / \\thesubsection must use \\textenglish for LTR digits."""
    assert r"\renewcommand{\thesection}{\textenglish" in article.main_tex, (
        f"[{article.name}] \\thesection not wrapped in \\textenglish"
    )
    assert r"\renewcommand{\thesubsection}{\textenglish" in article.main_tex, (
        f"[{article.name}] \\thesubsection not wrapped in \\textenglish"
    )


# ---------------------------------------------------------------------------
# 4. Required Elements
# ---------------------------------------------------------------------------

def test_has_table(article: ArticleData) -> None:
    """At least one \\begin{table} environment must exist in chapter sources."""
    ch_text = _all_chapter_text(article)
    count = len(re.findall(r"\\begin\{table", ch_text))
    assert count >= 1, (
        f"[{article.name}] No \\begin{{table}} found in chapters ({count})"
    )


def test_has_math_formula(article: ArticleData) -> None:
    """At least one display-math environment (equation, align, etc.) must exist."""
    ch_text = _all_chapter_text(article)
    patterns = [
        r"\\begin\{equation\}",
        r"\\begin\{align\}",
        r"\\begin\{align\*\}",
        r"\\begin\{gather\}",
        r"\$\$",
    ]
    total = sum(len(re.findall(p, ch_text)) for p in patterns)
    assert total >= 1, (
        f"[{article.name}] No display-math environments found ({total})"
    )


def test_has_python_generated_graph(article: ArticleData) -> None:
    """assets/results_graph.png (matplotlib-generated) must be included in a chapter."""
    ch_text = _all_chapter_text(article)
    assert "results_graph.png" in ch_text, (
        f"[{article.name}] results_graph.png not embedded in any chapter"
    )
    # The PNG must actually exist on disk
    graph_path = ARTICLES[article.name] / "assets" / "results_graph.png"
    assert graph_path.exists(), (
        f"[{article.name}] assets/results_graph.png file is missing from disk"
    )


def test_has_architecture_figure(article: ArticleData) -> None:
    """assets/architecture.png (matplotlib-generated) must be included in a chapter."""
    ch_text = _all_chapter_text(article)
    assert "architecture.png" in ch_text, (
        f"[{article.name}] architecture.png not embedded in any chapter"
    )
    graph_path = ARTICLES[article.name] / "assets" / "architecture.png"
    assert graph_path.exists(), (
        f"[{article.name}] assets/architecture.png file is missing from disk"
    )


def test_image_count_in_pdf(article: ArticleData) -> None:
    """Each PDF should contain at least 2 embedded raster images."""
    total_images = sum(
        len(page.get_images(full=False))
        for page in article.pdf
    )
    assert total_images >= 2, (
        f"[{article.name}] Only {total_images} images found in PDF (expected ≥ 2)"
    )


# ---------------------------------------------------------------------------
# 5. Data-Chained Citations
# ---------------------------------------------------------------------------

def test_all_cite_keys_in_bib(article: ArticleData) -> None:
    """Every \\cite{key} in chapters must resolve to a key in refs.bib."""
    missing = _cite_keys(article) - _bib_keys(article)
    assert not missing, (
        f"[{article.name}] \\cite keys not found in refs.bib: {sorted(missing)}"
    )


def test_bibliography_not_empty(article: ArticleData) -> None:
    """refs.bib must have at least 5 entries."""
    count = len(_bib_keys(article))
    assert count >= 5, (
        f"[{article.name}] refs.bib has only {count} entries (expected ≥ 5)"
    )


def test_no_undefined_citation_in_log(article: ArticleData) -> None:
    """LaTeX log must not contain 'Citation ... undefined' warnings."""
    matches = re.findall(r"Citation `([^']+)' .* undefined", article.latex_log)
    assert not matches, (
        f"[{article.name}] LaTeX reported undefined citations: {matches}"
    )


def test_no_missing_biblatex_entry_in_log(article: ArticleData) -> None:
    """biblatex log must not report missing entries."""
    pat = r"WARN.*entry could not be found|entry could not be found"
    bad = re.findall(pat, article.latex_log, re.I)
    assert not bad, (
        f"[{article.name}] biblatex reported missing entries in log"
    )


# ---------------------------------------------------------------------------
# 6. Visual Anomalies
# ---------------------------------------------------------------------------

def test_no_overfull_hbox(article: ArticleData) -> None:
    """LaTeX log must not contain Overfull \\hbox (text overflow) entries."""
    matches = re.findall(r"Overfull \\hbox.*?\n", article.latex_log)
    assert not matches, (
        f"[{article.name}] {len(matches)} Overfull \\hbox entries: {matches[:3]}"
    )


def test_underfull_hbox_count(article: ArticleData) -> None:
    """Underfull \\hbox count must be ≤ 5 (> 5 flags spacing issues)."""
    matches = re.findall(r"Underfull \\hbox", article.latex_log)
    assert len(matches) <= 5, (
        f"[{article.name}] {len(matches)} Underfull \\hbox entries (threshold: 5)"
    )


def test_no_latex_errors(article: ArticleData) -> None:
    """LaTeX log must not contain fatal ! errors."""
    errors = re.findall(r"^!.*", article.latex_log, re.MULTILINE)
    assert not errors, (
        f"[{article.name}] LaTeX errors found: {errors[:5]}"
    )


def test_no_duplicate_chapter_inputs(article: ArticleData) -> None:
    """main.tex must not \\input any chapter more than once (padding artifact)."""
    inputs = re.findall(r"\\input\{(chapters/ch\d+)\}", article.main_tex)
    duplicates = {ch for ch in inputs if inputs.count(ch) > 1}
    assert not duplicates, (
        f"[{article.name}] Duplicate \\input entries in main.tex: {sorted(duplicates)} "
        "(chapters included multiple times to artificially inflate page count)"
    )


def test_no_tikz_anchor_warnings(article: ArticleData) -> None:
    """LaTeX log must not warn about unknown TikZ anchors."""
    pat = r"pgf.*anchor.*not defined|Unknown anchor|I don't know.*anchor"
    bad = re.findall(pat, article.latex_log, re.I)
    assert not bad, (
        f"[{article.name}] TikZ anchor/positioning warnings: {bad[:3]}"
    )


# ---------------------------------------------------------------------------
# Orphan / unused bib entries (informational, non-fatal via xfail)
# ---------------------------------------------------------------------------

@pytest.mark.xfail(reason="Orphan bib entries: informational only", strict=False)
def test_no_orphan_bib_entries(article: ArticleData) -> None:
    """Every key in refs.bib should be cited at least once (no orphans)."""
    orphans = _bib_keys(article) - _cite_keys(article)
    assert not orphans, (
        f"[{article.name}] Orphan bib entries never \\cited: {sorted(orphans)}"
    )
