#!/usr/bin/env python3
"""Assemble 4 research articles from templates/ into results/."""
from pathlib import Path

TEMPLATES = Path("templates")
ARTICLES = [
    ("1_sine_wave",     "refs.bib", ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6"]),
    ("2_security",      "refs.bib", ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6"]),
    ("3_xlstm",         "refs.bib", ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6"]),
    ("4_orchestration", "refs.bib", ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6"]),
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: str, content: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _main_tex(article: str, bib: str, chapters: list) -> str:
    tmpl = TEMPLATES / article
    preamble = _read(TEMPLATES / "preamble.tex")
    meta = _read(tmpl / "meta.tex")
    parts = [
        preamble,
        f"\\addbibresource{{{bib}}}\n",
        meta,
        "\\begin{document}\n\\maketitle\n\\tableofcontents\n\\newpage\n",
    ]
    for ch in chapters:
        parts.append(f"\\input{{chapters/{ch}}}\n")
    parts.extend([
        "\n\\newpage\n\\chapter*{ביבליוגרפיה}\n",
        "\\begin{english}\n\\sloppy\n\\printbibliography[heading=none]\n",
        "\\end{english}\n\\end{document}\n",
    ])
    return "".join(parts)


def build_article(article: str, bib: str, chapters: list) -> None:
    tmpl = TEMPLATES / article
    base = Path("results") / article
    _write(f"{base}/refs.bib", _read(tmpl / "refs.bib"))
    for ch in chapters:
        _write(f"{base}/chapters/{ch}.tex", _read(tmpl / f"{ch}.tex"))
    _write(f"{base}/main.tex", _main_tex(article, bib, chapters))
    print(f"Built {article}")


if __name__ == "__main__":
    for article, bib, chapters in ARTICLES:
        build_article(article, bib, chapters)
