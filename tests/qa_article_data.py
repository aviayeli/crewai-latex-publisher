"""Shared data types and helpers for QA sweep tests."""

from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

import fitz  # PyMuPDF

RESULTS_ROOT = Path(__file__).parent.parent / "results"
ARTICLES = {
    "1_sine_wave": RESULTS_ROOT / "1_sine_wave",
    "2_security": RESULTS_ROOT / "2_security",
    "3_xlstm": RESULTS_ROOT / "3_xlstm",
    "4_orchestration": RESULTS_ROOT / "4_orchestration",
}
MIN_PAGES = 15


class ArticleData(NamedTuple):
    name: str
    pdf: fitz.Document
    main_tex: str
    chapters_tex: dict[str, str]
    refs_bib: str
    latex_log: str


def load_article(name: str, root: Path) -> ArticleData:
    pdf = fitz.open(root / "main.pdf")
    main_tex = (root / "main.tex").read_text(encoding="utf-8")
    chapters: dict[str, str] = {}
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


def all_chapter_text(data: ArticleData) -> str:
    return "\n".join(data.chapters_tex.values())


def bib_keys(data: ArticleData) -> set[str]:
    return set(re.findall(r"@\w+\{([^,]+),", data.refs_bib))


def cite_keys(data: ArticleData) -> set[str]:
    raw = re.findall(r"\\cite\{([^}]+)\}", all_chapter_text(data))
    keys: set[str] = set()
    for group in raw:
        for k in group.split(","):
            keys.add(k.strip())
    return keys
