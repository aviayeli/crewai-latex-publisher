"""QA sweep — page count, headers, footers (requires pre-built PDFs)."""

from __future__ import annotations

import re

import pytest

from tests.qa_article_data import MIN_PAGES, ArticleData

pytestmark = pytest.mark.slow


def test_minimum_page_count(article: ArticleData) -> None:
    """PDF must be at least 15 pages."""
    actual = len(article.pdf)
    assert actual >= MIN_PAGES, (
        f"[{article.name}] Only {actual} pages — minimum is {MIN_PAGES}"
    )


def test_headers_present(article: ArticleData) -> None:
    """At least half the content pages must carry a non-empty running header."""
    pages_with_header = 0
    for page in article.pdf:
        for _x0, y0, _x1, _y1, text, *_ in page.get_text("blocks"):
            if y0 < 80 and text.strip():
                pages_with_header += 1
                break
    content_pages = max(1, len(article.pdf) - 2)
    assert pages_with_header >= content_pages * 0.5, (
        f"[{article.name}] Headers on only {pages_with_header} pages "
        f"(expected ≥ {content_pages * 0.5:.0f} of {content_pages})"
    )


def test_footers_present(article: ArticleData) -> None:
    """Every page (except perhaps the first) should have a page-number footer."""
    pages = list(article.pdf)
    height = pages[0].rect.height
    pages_with_footer = 0
    for page in pages:
        for _x0, _y0, _x1, y1, text, *_ in page.get_text("blocks"):
            if y1 > height - 60 and re.search(r"\d+", text):
                pages_with_footer += 1
                break
    assert pages_with_footer >= len(pages) - 1, (
        f"[{article.name}] Footer missing on "
        f"{len(pages) - pages_with_footer} pages"
    )


def test_plain_pagestyle_override_in_preamble(article: ArticleData) -> None:
    r"""\\fancypagestyle{plain} override must be defined in main.tex."""
    assert "fancypagestyle{plain}" in article.main_tex, (
        f"[{article.name}] Missing \\fancypagestyle{{plain}} override"
    )
