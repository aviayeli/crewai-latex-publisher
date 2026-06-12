#!/usr/bin/env python3
"""Assemble and compile 4 research articles from templates/ into results/."""
import os
import re
import subprocess
from pathlib import Path

_LUALATEX = os.environ.get("LUALATEX_BIN", "lualatex")
_BIBER = os.environ.get("BIBER_BIN", "biber")

TEMPLATES = Path("templates")
_CH9  = [f"ch{i}" for i in range(1, 10)]
_CH10 = [f"ch{i}" for i in range(1, 11)]

ARTICLES = [
    ("1_sine_wave",     "refs.bib", _CH9),
    ("2_security",      "refs.bib", _CH10),
    ("3_xlstm",         "refs.bib", _CH10),
    ("4_orchestration", "refs.bib", _CH10),
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


# ── Citation sync helpers ──────────────────────────────────────────────────────

def _bib_keys(bib_content: str) -> set:
    """Return all BibTeX keys defined in a .bib file."""
    return {m.group(1).strip() for m in re.finditer(r"@\w+\{([^,\s]+)\s*,", bib_content)}


def _cite_keys(tex_content: str) -> set:
    r"""Return all citation keys used in \cite{} commands in a .tex file."""
    keys = set()
    for m in re.finditer(r"\\cite\{([^}]+)\}", tex_content):
        for k in m.group(1).split(","):
            keys.add(k.strip())
    return keys


def _remove_missing_cites(tex: str, defined: set) -> tuple:
    r"""Remove \cite{} calls whose keys are absent from defined. Returns (fixed_tex, removed_keys)."""
    removed = []

    def _fix(raw_keys):
        valid = [k.strip() for k in raw_keys.split(",") if k.strip() in defined]
        bad   = [k.strip() for k in raw_keys.split(",") if k.strip() not in defined]
        removed.extend(bad)
        return ",".join(valid) if valid else None

    def _repl_tilde(m):
        result = _fix(m.group(1))
        return f"~\\cite{{{result}}}" if result else ""

    def _repl_plain(m):
        result = _fix(m.group(1))
        return f"\\cite{{{result}}}" if result else ""

    tex = re.sub(r"~\\cite\{([^}]+)\}", _repl_tilde, tex)
    tex = re.sub(r"\\cite\{([^}]+)\}",  _repl_plain, tex)
    return tex, removed


def _prune_orphan_bibs(bib: str, cited: set) -> tuple:
    """Remove bib entries never cited. Returns (pruned_bib, pruned_keys)."""
    pruned = []
    entries = re.split(r"(?=@\w+\{)", bib)
    kept = []
    for entry in entries:
        if not entry.strip():
            continue
        m = re.match(r"@\w+\{([^,\s]+)\s*,", entry)
        if m:
            key = m.group(1).strip()
            if key in cited:
                kept.append(entry)
            else:
                pruned.append(key)
        else:
            kept.append(entry)
    return "".join(kept), pruned


def sync_citations(base: Path) -> None:
    r"""Sync citations: remove broken \cite{} keys, prune orphan bib entries."""
    bib_path = base / "refs.bib"
    chapters_dir = base / "chapters"
    if not bib_path.exists():
        return

    defined = _bib_keys(_read(bib_path))
    all_cited: set = set()

    for tex_file in sorted(chapters_dir.glob("*.tex")):
        content = _read(tex_file)
        fixed, removed = _remove_missing_cites(content, defined)
        if removed:
            print(f"  [CITE-SYNC] {tex_file.name}: removed missing keys {removed}")
            tex_file.write_text(fixed, encoding="utf-8")
            content = fixed
        all_cited |= _cite_keys(content)

    pruned_bib, pruned_keys = _prune_orphan_bibs(_read(bib_path), all_cited)
    if pruned_keys:
        print(f"  [CITE-SYNC] refs.bib: pruned orphan entries {pruned_keys}")
        bib_path.write_text(pruned_bib, encoding="utf-8")


# ── Compilation ────────────────────────────────────────────────────────────────

def compile_article(base: Path) -> None:
    """Run lualatex→biber→lualatex→lualatex compilation inside base dir."""
    lualatex_cmd = [_LUALATEX, "-interaction=nonstopmode", "main.tex"]
    biber_cmd = [_BIBER, "main"]
    for cmd in [lualatex_cmd, biber_cmd, lualatex_cmd, lualatex_cmd]:
        subprocess.run(cmd, cwd=base, check=True)


def build_article(article: str, bib: str, chapters: list) -> None:
    tmpl = TEMPLATES / article
    base = Path("results") / article
    _write(f"{base}/refs.bib", _read(tmpl / "refs.bib"))
    for ch in chapters:
        _write(f"{base}/chapters/{ch}.tex", _read(tmpl / f"{ch}.tex"))
    _write(f"{base}/main.tex", _main_tex(article, bib, chapters))
    print(f"[CHECKPOINT] Step 1/3 done: {article} assembled. Running citation sync...")
    sync_citations(base)
    print(f"[CHECKPOINT] Step 2/3 done: {article} citations synced. Compiling...")
    compile_article(base)
    print(f"[CHECKPOINT] Step 3/3 done: {article} → results/{article}/main.pdf")


if __name__ == "__main__":
    for article, bib, chapters in ARTICLES:
        build_article(article, bib, chapters)
