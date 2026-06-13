"""Shared helpers: citation-sync between .tex chapter files and refs.bib."""

import re
from pathlib import Path


def _bib_keys(bib_content: str) -> set:
    """Return all BibTeX keys defined in a .bib file."""
    pat = r"@\w+\{([^,\s]+)\s*,"
    return {m.group(1).strip() for m in re.finditer(pat, bib_content)}


def _cite_keys(tex_content: str) -> set:
    r"""Return all citation keys used in \cite{} commands in a .tex file."""
    keys = set()
    for m in re.finditer(r"\\cite\{([^}]+)\}", tex_content):
        for k in m.group(1).split(","):
            keys.add(k.strip())
    return keys


def _remove_missing_cites(tex: str, defined: set) -> tuple:
    r"""Remove \cite{} calls absent from defined. Return (fixed_tex, removed_keys)."""
    removed: list = []

    def _fix(raw_keys: str) -> str | None:
        valid = [k.strip() for k in raw_keys.split(",") if k.strip() in defined]
        bad = [k.strip() for k in raw_keys.split(",") if k.strip() not in defined]
        removed.extend(bad)
        return ",".join(valid) if valid else None

    def _repl_tilde(m: re.Match) -> str:
        result = _fix(m.group(1))
        return f"~\\cite{{{result}}}" if result else ""

    def _repl_plain(m: re.Match) -> str:
        result = _fix(m.group(1))
        return f"\\cite{{{result}}}" if result else ""

    tex = re.sub(r"~\\cite\{([^}]+)\}", _repl_tilde, tex)
    tex = re.sub(r"\\cite\{([^}]+)\}", _repl_plain, tex)
    return tex, removed


def _prune_orphan_bibs(bib: str, cited: set) -> tuple:
    """Remove bib entries never cited. Returns (pruned_bib, pruned_keys)."""
    pruned: list = []
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

    bib_text = bib_path.read_text(encoding="utf-8")
    defined = _bib_keys(bib_text)
    all_cited: set = set()

    for tex_file in sorted(chapters_dir.glob("*.tex")):
        content = tex_file.read_text(encoding="utf-8")
        fixed, removed = _remove_missing_cites(content, defined)
        if removed:
            print(f"  [CITE-SYNC] {tex_file.name}: removed missing keys {removed}")
            tex_file.write_text(fixed, encoding="utf-8")
            content = fixed
        all_cited |= _cite_keys(content)

    pruned_bib, pruned_keys = _prune_orphan_bibs(bib_text, all_cited)
    if pruned_keys:
        print(f"  [CITE-SYNC] refs.bib: pruned orphan entries {pruned_keys}")
        bib_path.write_text(pruned_bib, encoding="utf-8")
