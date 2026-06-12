"""QA sweep — LaTeX log anomalies and structure checks (requires pre-built PDFs)."""

from __future__ import annotations

import re

import pytest

from tests.qa_article_data import ArticleData

pytestmark = pytest.mark.slow


def test_no_overfull_hbox(article: ArticleData) -> None:
    r"""LaTeX log must not contain Overfull \hbox entries."""
    matches = re.findall(r"Overfull \\hbox.*?\n", article.latex_log)
    assert not matches, (
        f"[{article.name}] {len(matches)} Overfull \\hbox: {matches[:3]}"
    )


def test_underfull_hbox_count(article: ArticleData) -> None:
    r"""Underfull \hbox count must be ≤ 5."""
    matches = re.findall(r"Underfull \\hbox", article.latex_log)
    assert len(matches) <= 5, (
        f"[{article.name}] {len(matches)} Underfull \\hbox (threshold: 5)"
    )


def test_no_latex_errors(article: ArticleData) -> None:
    """LaTeX log must not contain fatal ! errors."""
    errors = re.findall(r"^!.*", article.latex_log, re.MULTILINE)
    assert not errors, (
        f"[{article.name}] LaTeX errors: {errors[:5]}"
    )


def test_no_duplicate_chapter_inputs(article: ArticleData) -> None:
    r"""main.tex must not \input any chapter more than once."""
    inputs = re.findall(r"\\input\{(chapters/ch\d+)\}", article.main_tex)
    duplicates = {ch for ch in inputs if inputs.count(ch) > 1}
    assert not duplicates, (
        f"[{article.name}] Duplicate \\input entries: {sorted(duplicates)}"
    )


def test_no_tikz_anchor_warnings(article: ArticleData) -> None:
    """LaTeX log must not warn about unknown TikZ anchors."""
    pat = r"pgf.*anchor.*not defined|Unknown anchor|I don't know.*anchor"
    bad = re.findall(pat, article.latex_log, re.I)
    assert not bad, (
        f"[{article.name}] TikZ anchor warnings: {bad[:3]}"
    )
