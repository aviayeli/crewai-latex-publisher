"""
fix_bidi_decimals.py — Retroactive BidiAgent: wrap bare decimal numbers in math mode.

Rule (SKILL.md §Validation Checklist #13):
  Any decimal number matching \\d+\\.\\d+ that is NOT already inside
  math mode, \\textenglish{}, \\begin{LTR}, or \\begin{english} must
  be wrapped as $N.N$ to prevent RTL BiDi reversal (e.g. 3.14 → 14.3).
"""

import re
import sys
from pathlib import Path

CHAPTER_DIR = Path("latex_output/chapters")
DECIMAL_RE = re.compile(r"(?<!\w)(\d+\.\d+)(?!\w)")

# Dimension suffixes that must NOT be wrapped (LaTeX lengths)
DIMENSION_UNITS = re.compile(
    r"\d+\.\d+\s*(pt|em|ex|cm|mm|in|bp|dd|cc|sp|mu)\b"
)


def is_safe_context(line: str, match_start: int) -> bool:
    """Return True if the decimal at match_start is already in a safe LTR context."""
    before = line[:match_start]

    # Already inside \textenglish{...}
    if "\\textenglish{" in before:
        opens = [m.start() for m in re.finditer(r"\\textenglish\{", before)]
        if opens:
            tail = before[opens[-1]:]
            if tail.count("{") > tail.count("}"):
                return True

    # Inside inline math \(...\)
    if re.search(r"\\\((?:[^)\\]|\\.)*$", before):
        return True

    # Inside $...$ — count unescaped $ signs
    dollar_count = len(re.findall(r"(?<!\\)\$", before))
    if dollar_count % 2 == 1:
        return True

    # Inside a LaTeX command argument (backslash-word followed by {)
    return bool(re.search(r"\\[a-zA-Z@]+\{[^}]*$", before))


def process_file(path: Path, dry_run: bool = False) -> list[str]:
    """Process a single .tex file. Returns list of change descriptions."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    changes = []
    in_ltr = False
    in_math_env = False
    new_lines = []

    math_open = re.compile(
        r"\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}"
    )
    math_close = re.compile(
        r"\\end\{(equation\*?|align\*?|gather\*?|multline\*?)\}"
    )

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track environment state
        if "\\begin{LTR}" in line or "\\begin{english}" in line:
            in_ltr = True
        if "\\end{LTR}" in line or "\\end{english}" in line:
            in_ltr = False
        if math_open.search(line):
            in_math_env = True
        if math_close.search(line):
            in_math_env = False

        # Skip lines we must not touch
        skip = (
            stripped.startswith("%")
            or in_ltr
            or in_math_env
            or "\\includegraphics" in line
            or "\\label{" in line
            or "\\ref{" in line
            or "\\hyperref" in line
            or bool(DIMENSION_UNITS.search(line))
        )

        if skip:
            new_lines.append(line)
            continue

        new_line = line
        offset = 0
        for m in DECIMAL_RE.finditer(line):
            adjusted_start = m.start() + offset
            if is_safe_context(new_line, adjusted_start):
                continue
            decimal = m.group()
            replacement = f"${decimal}$"
            end = adjusted_start + len(decimal)
            new_line = new_line[:adjusted_start] + replacement + new_line[end:]
            offset += len(replacement) - len(decimal)
            changes.append(
                f"  {path.name}:{lineno}: {decimal!r} -> {replacement!r}"
            )

        new_lines.append(new_line)

    if changes and not dry_run:
        path.write_text("".join(new_lines), encoding="utf-8")

    return changes


def main():
    dry_run = "--dry-run" in sys.argv
    tex_files = sorted(CHAPTER_DIR.glob("*.tex"))

    print(f"fix_bidi_decimals.py — scanning {len(tex_files)} chapter files")
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLY FIXES'}")
    print()

    total = 0
    for f in tex_files:
        changes = process_file(f, dry_run=dry_run)
        if changes:
            print(f"[CHANGED] {f.name}: {len(changes)} decimal(s) wrapped")
            for c in changes:
                print(c)
            total += len(changes)
        else:
            print(f"[CLEAN]   {f.name}: no bare decimals found")

    print()
    if total == 0:
        print("RESULT: All files clean — no decimal reversal bugs detected.")
    else:
        count = len(tex_files)
        print(f"RESULT: {total} decimal(s) wrapped in math mode across {count} files.")
        if dry_run:
            print("(DRY RUN — no files modified. Re-run without --dry-run to apply.)")


if __name__ == "__main__":
    main()
