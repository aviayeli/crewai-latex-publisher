"""QA sweep — citation integrity checks (requires pre-built PDFs)."""

from __future__ import annotations

import re

import pytest

from tests.qa_article_data import ArticleData, bib_keys, cite_keys

pytestmark = pytest.mark.slow


def test_all_cite_keys_in_bib(article: ArticleData) -> None:
    r"""Every \cite{key} in chapters must resolve to a key in refs.bib."""
    missing = cite_keys(article) - bib_keys(article)
    assert not missing, (
        f"[{article.name}] \\cite keys missing from refs.bib: {sorted(missing)}"
    )


def test_bibliography_not_empty(article: ArticleData) -> None:
    """refs.bib must have at least 5 entries."""
    count = len(bib_keys(article))
    assert count >= 5, (
        f"[{article.name}] refs.bib has only {count} entries (expected ≥ 5)"
    )


def test_no_undefined_citation_in_log(article: ArticleData) -> None:
    """LaTeX log must not contain 'Citation ... undefined' warnings."""
    matches = re.findall(r"Citation `([^']+)' .* undefined", article.latex_log)
    assert not matches, (
        f"[{article.name}] Undefined citations in log: {matches}"
    )


def test_no_missing_biblatex_entry_in_log(article: ArticleData) -> None:
    """biblatex log must not report missing entries."""
    pat = r"WARN.*entry could not be found|entry could not be found"
    bad = re.findall(pat, article.latex_log, re.I)
    assert not bad, (
        f"[{article.name}] biblatex missing-entry warnings in log"
    )


@pytest.mark.xfail(reason="Orphan bib entries: informational only", strict=False)
def test_no_orphan_bib_entries(article: ArticleData) -> None:
    """Every key in refs.bib should be cited at least once (no orphans)."""
    orphans = bib_keys(article) - cite_keys(article)
    assert not orphans, (
        f"[{article.name}] Orphan bib entries never \\cited: {sorted(orphans)}"
    )
