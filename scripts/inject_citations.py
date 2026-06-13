"""
inject_citations.py — Retroactively inject \\cite{} commands into chapter .tex files.

Adds ~\\cite{key} before sentence-ending periods at specific claim locations
to satisfy Criterion 1.9 (Data-Chained Citations). Target: 15-20 total injections.
"""

import re
import sys
from pathlib import Path

from scripts.citation_rules import CHAPTER_DIR, RULES


def parse_bib_keys(bib_path: Path) -> set[str]:
    """Extract all citation keys from a .bib file."""
    keys = set()
    for m in re.finditer(r"^@\w+\{([^,\s]+)", bib_path.read_text(), re.MULTILINE):
        keys.add(m.group(1))
    return keys


def count_cites(text: str) -> int:
    return len(re.findall(r"\\cite\{", text))


def apply_rules(
    rules: list[tuple[str, str, str]],
    dry_run: bool = False,
) -> dict[str, int]:
    """Apply citation injection rules. Returns {filename: injections_count}."""
    by_file: dict[str, list[tuple[str, str]]] = {}
    for fname, old, new in rules:
        by_file.setdefault(fname, []).append((old, new))

    results: dict[str, int] = {}
    for fname, file_rules in by_file.items():
        path = CHAPTER_DIR / fname
        if not path.exists():
            print(f"[SKIP]    {fname}: file not found")
            continue
        text = path.read_text(encoding="utf-8")
        before = count_cites(text)
        for old, new in file_rules:
            if old in text:
                text = text.replace(old, new, 1)
            else:
                print(f"  [MISS]  {fname}: {old[:50]!r} not found")
        after = count_cites(text)
        injected = after - before
        results[fname] = injected
        if injected and not dry_run:
            path.write_text(text, encoding="utf-8")
    return results


def main() -> None:
    bib = Path("latex_output/refs.bib")
    if bib.exists():
        valid_keys = parse_bib_keys(bib)
        all_used: set[str] = set()
        for _, _, new in RULES:
            for m in re.finditer(r"\\cite\{([^}]+)\}", new):
                all_used.update(m.group(1).split(","))
        missing = all_used - valid_keys
        if missing:
            print(f"WARNING: these keys are not in refs.bib: {missing}")

    dry_run = "--dry-run" in sys.argv
    print(f"inject_citations.py — {len(RULES)} rules across 6 chapters")
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLY'}\n")

    results = apply_rules(RULES, dry_run=dry_run)
    total = sum(results.values())
    for fname, n in results.items():
        print(f"[{'CHANGED' if n else 'CLEAN':8s}] {fname}: {n} cite(s) injected")

    print(f"\nRESULT: {total} citation(s) injected across {len(results)} files.")
    if dry_run:
        print("(DRY RUN — no files modified)")


if __name__ == "__main__":
    main()
