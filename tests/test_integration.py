import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.slow

_has_api_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
_has_lualatex = shutil.which("lualatex") is not None

skip_unless_ready = pytest.mark.skipif(
    not (_has_api_key and _has_lualatex),
    reason="Requires ANTHROPIC_API_KEY env var and lualatex binary",
)


@skip_unless_ready
def test_full_pipeline_produces_pdf():
    from src.crew import PublisherCrew

    PublisherCrew().kickoff()
    assert Path("latex_output/main.pdf").exists()


@skip_unless_ready
def test_pdf_has_minimum_fifteen_pages():
    if not shutil.which("pdfinfo"):
        pytest.skip("pdfinfo not available")
    result = subprocess.run(
        ["pdfinfo", "latex_output/main.pdf"],
        capture_output=True,
        text=True,
        check=True,
    )
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            pages = int(line.split(":")[1].strip())
            assert pages >= 15, f"PDF has only {pages} pages, expected >= 15"
            return
    pytest.fail("Could not parse page count from pdfinfo output")


def test_all_six_chapter_files_exist():
    chapters = Path("latex_output/chapters")
    for n in range(1, 7):
        assert (chapters / f"ch{n}.tex").exists(), f"ch{n}.tex missing"


def test_book_outline_json_is_valid_json():
    outline = Path("latex_output/book_outline.json")
    assert outline.exists()
    with outline.open() as f:
        json.load(f)


def test_book_outline_has_six_chapters():
    with Path("latex_output/book_outline.json").open() as f:
        data = json.load(f)
    assert len(data["chapters"]) == 6


def test_attention_complexity_png_exists():
    assert Path("latex_output/assets/attention_complexity.png").exists()


def test_sdp_attention_tex_exists():
    assert Path("latex_output/figures/sdp_attention.tex").exists()


def test_main_tex_contains_six_input_commands():
    text = Path("latex_output/main.tex").read_text()
    count = text.count(r"\input{")
    assert count == 6, f"Expected 6 \\input{{}} commands, found {count}"
