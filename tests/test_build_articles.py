"""TDD tests for build_articles.py assembly logic.

Run BEFORE fixing build_articles.py to see red → green cycle.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from build_articles import _main_tex  # noqa: E402

_PREAMBLE = (Path(__file__).parent.parent / "templates" / "preamble.tex").read_text()


def test_preamble_template_has_addbibresource():
    """templates/preamble.tex must own the single \\addbibresource declaration."""
    assert "\\addbibresource" in _PREAMBLE, (
        "templates/preamble.tex is missing \\addbibresource{refs.bib}. "
        "The preamble must declare the bib resource; "
        "build_articles.py must NOT inject a second one."
    )


def test_no_duplicate_addbibresource():
    """Assembled main.tex must contain exactly one \\addbibresource."""
    result = _main_tex("1_sine_wave", "refs.bib", ["ch1"])
    count = result.count("\\addbibresource")
    assert count == 1, (
        f"Expected exactly 1 \\addbibresource but found {count}. "
        "build_articles.py is injecting a duplicate that crashes Biber."
    )


def test_printbibliography_present():
    """Assembled main.tex must contain \\printbibliography before \\end{document}."""
    result = _main_tex("1_sine_wave", "refs.bib", ["ch1"])
    bib_pos = result.rfind("\\printbibliography")
    end_pos = result.rfind("\\end{document}")
    assert bib_pos != -1, "\\printbibliography missing from generated main.tex"
    assert bib_pos < end_pos, "\\printbibliography must appear before \\end{document}"


def test_documentclass_present():
    """Assembled main.tex must contain \\documentclass (sourced from preamble.tex)."""
    result = _main_tex("1_sine_wave", "refs.bib", ["ch1"])
    assert "\\documentclass" in result


def test_six_chapter_inputs_generated():
    """All requested chapters must appear as \\input{} calls."""
    chapters = [f"ch{i}" for i in range(1, 7)]
    result = _main_tex("1_sine_wave", "refs.bib", chapters)
    for ch in chapters:
        assert f"\\input{{chapters/{ch}}}" in result
