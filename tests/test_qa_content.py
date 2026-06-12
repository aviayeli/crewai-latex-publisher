"""QA sweep — required content elements (requires pre-built PDFs)."""

from __future__ import annotations

import re

import pytest

from tests.qa_article_data import ARTICLES, ArticleData, all_chapter_text

pytestmark = pytest.mark.slow


def test_has_table(article: ArticleData) -> None:
    r"""At least one \begin{table} must exist in chapter sources."""
    count = len(re.findall(r"\\begin\{table", all_chapter_text(article)))
    assert count >= 1, (
        f"[{article.name}] No \\begin{{table}} found ({count})"
    )


def test_has_math_formula(article: ArticleData) -> None:
    """At least one display-math environment must exist."""
    patterns = [
        r"\\begin\{equation\}",
        r"\\begin\{align\}",
        r"\\begin\{align\*\}",
        r"\\begin\{gather\}",
        r"\$\$",
    ]
    ch = all_chapter_text(article)
    total = sum(len(re.findall(p, ch)) for p in patterns)
    assert total >= 1, (
        f"[{article.name}] No display-math environments found ({total})"
    )


def test_has_python_generated_graph(article: ArticleData) -> None:
    """assets/results_graph.png must be embedded and exist on disk."""
    ch = all_chapter_text(article)
    assert "results_graph.png" in ch, (
        f"[{article.name}] results_graph.png not embedded in any chapter"
    )
    graph = ARTICLES[article.name] / "assets" / "results_graph.png"
    assert graph.exists(), (
        f"[{article.name}] assets/results_graph.png missing from disk"
    )


def test_has_architecture_figure(article: ArticleData) -> None:
    """assets/architecture.png must be embedded and exist on disk."""
    ch = all_chapter_text(article)
    assert "architecture.png" in ch, (
        f"[{article.name}] architecture.png not embedded in any chapter"
    )
    fig = ARTICLES[article.name] / "assets" / "architecture.png"
    assert fig.exists(), (
        f"[{article.name}] assets/architecture.png missing from disk"
    )


def test_image_count_in_pdf(article: ArticleData) -> None:
    """PDF must contain at least 2 embedded raster images."""
    total = sum(len(page.get_images(full=False)) for page in article.pdf)
    assert total >= 2, (
        f"[{article.name}] Only {total} images in PDF (expected ≥ 2)"
    )
