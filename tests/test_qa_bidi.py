"""QA sweep — BiDi integrity checks (requires pre-built PDFs)."""

from __future__ import annotations

import re

import pytest

from tests.qa_article_data import ArticleData

pytestmark = pytest.mark.slow


def test_thepage_wrapped_in_textenglish(article: ArticleData) -> None:
    r"""\\thepage must be redefined with \textenglish for LTR page digits."""
    needle = r"\renewcommand{\thepage}{\textenglish{\arabic{page}}}"
    assert needle in article.main_tex, (
        f"[{article.name}] \\thepage not wrapped — digits may reverse in RTL"
    )


def test_page_numbers_are_decimal(article: ArticleData) -> None:
    """Footer page-number tokens must be plain decimal integers."""
    pages = list(article.pdf)
    height = pages[0].rect.height
    bad_pages: list[int] = []
    for i, page in enumerate(pages, start=1):
        for _x0, _y0, _x1, y1, text, *_ in page.get_text("blocks"):
            if y1 > height - 60:
                stripped = text.strip()
                if stripped and not re.fullmatch(r"\d+", stripped):
                    tokens = stripped.split()
                    page_token = tokens[-1] if tokens else ""
                    if page_token and not re.fullmatch(r"\d+", page_token):
                        bad_pages.append(i)
    assert not bad_pages, (
        f"[{article.name}] Non-decimal page tokens on pages: {bad_pages}"
    )


def test_section_numbers_use_textenglish(article: ArticleData) -> None:
    r"""\\thesection / \\thesubsection must use \\textenglish for LTR digits."""
    assert r"\renewcommand{\thesection}{\textenglish" in article.main_tex, (
        f"[{article.name}] \\thesection not wrapped in \\textenglish"
    )
    assert r"\renewcommand{\thesubsection}{\textenglish" in article.main_tex, (
        f"[{article.name}] \\thesubsection not wrapped in \\textenglish"
    )
