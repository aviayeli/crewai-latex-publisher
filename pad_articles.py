#!/usr/bin/env python3
"""Add ch9 (related-work) to each article from templates/ and update main.tex."""
from pathlib import Path

TEMPLATES = Path("templates")
PADS = [
    ("1_sine_wave",     ["ch9"]),
    ("2_security",      ["ch9"]),
    ("3_xlstm",         ["ch9"]),
    ("4_orchestration", ["ch9"]),
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: str, content: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _append_chapters(main_tex_path: str, new_chapters: list) -> None:
    txt = _read(Path(main_tex_path))
    insert = "".join(f"\\input{{chapters/{c}}}\n" for c in new_chapters)
    txt = txt.replace(
        "\\newpage\n\\chapter*{ביבליוגרפיה}",
        insert + "\n\\newpage\n\\chapter*{ביבליוגרפיה}",
    )
    Path(main_tex_path).write_text(txt, encoding="utf-8")


def pad_article(article: str, chapters: list) -> None:
    base = Path("results") / article
    for ch in chapters:
        _write(f"{base}/chapters/{ch}.tex", _read(TEMPLATES / article / f"{ch}.tex"))
    _append_chapters(f"{base}/main.tex", chapters)
    print(f"Padded {article} (+{chapters})")


if __name__ == "__main__":
    for article, chapters in PADS:
        pad_article(article, chapters)
    print("All related-work chapters added.")
