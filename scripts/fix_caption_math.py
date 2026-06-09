"""
fix_caption_math.py — Retroactive fix: wrap math notation in \\caption{} and TikZ
\\node{} arguments that appear inside \\textenglish{} without math mode ($...$).

Targets the specific patterns that cause '! Missing $ inserted':
  \\textenglish{O(n \\log n)}         -> \\textenglish{$O(n \\log n)$}
  \\textenglish{O(n\\textsuperscript{2})} -> \\textenglish{$O(n^{2})$}
  \\textenglish{O(n²)}               -> \\textenglish{$O(n^{2})$}
  \\textenglish{O(n)}                -> \\textenglish{$O(n)$}
"""

import re
import sys
from pathlib import Path

CHAPTER_DIR = Path("latex_output/chapters")

# \\textenglish{content} where content has math notation but NO $ wrapping
MATH_OPS = re.compile(
    r"\\textenglish\{"
    r"(?!\$)"           # not already starting with $
    r"([^}]*"
    r"(?:\\log|\\sin|\\cos|\\tanh|\\sqrt|\\sum|\\prod|\\frac|\\textsuperscript|\^|_)"
    r"[^}]*)"
    r"\}",
)

# \\textenglish{O(n²)} — Unicode superscript digit
UNICODE_SUP_RE = re.compile(r"\\textenglish\{O\(n([²³⁴])\)\}")

# \\textenglish{O(n)} — bare Big-O without math operators (safe but make consistent)
BARE_ON_RE = re.compile(r"\\textenglish\{(O\([^$}]+\))\}(?!\$)")


def contains_math_op(content: str) -> bool:
    ops = (
        r"\log", r"\sin", r"\cos", r"\tanh", r"\sqrt",
        r"\sum", r"\prod", r"\frac", r"\textsuperscript",
    )
    return any(op in content for op in ops) or "^" in content or "_" in content


def fix_textenglish_math(line: str) -> str:
    """Wrap bare math inside \\textenglish{} with $...$."""
    # 1. Unicode superscript → LaTeX math
    def fix_unicode_sup(m: re.Match) -> str:
        sup_map = {"²": "2", "³": "3", "⁴": "4"}
        digit = sup_map.get(m.group(1), m.group(1))
        return rf"\textenglish{{$O(n^{{{digit}}})$}}"

    line = UNICODE_SUP_RE.sub(fix_unicode_sup, line)

    # 2. \\textenglish{content with math ops but no $}
    def fix_math_op(m: re.Match) -> str:
        content = m.group(1)
        # Replace \textsuperscript{N} -> ^{N}
        content = re.sub(r"\\textsuperscript\{([^}]+)\}", r"^{\1}", content)
        return rf"\textenglish{{${content}$}}"

    line = MATH_OPS.sub(fix_math_op, line)

    return line


def process_file(path: Path, dry_run: bool = False) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    changes = []
    new_lines = []

    for lineno, line in enumerate(lines, 1):
        new_line = fix_textenglish_math(line)
        if new_line != line:
            changes.append(
                f"  {path.name}:{lineno}: math mode wrapped"
            )
        new_lines.append(new_line)

    if changes and not dry_run:
        path.write_text("".join(new_lines), encoding="utf-8")

    return changes


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    tex_files = sorted(CHAPTER_DIR.glob("*.tex"))

    print(f"fix_caption_math.py — scanning {len(tex_files)} chapter files")
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLY FIXES'}")
    print()

    total = 0
    for f in tex_files:
        changes = process_file(f, dry_run=dry_run)
        if changes:
            print(f"[CHANGED] {f.name}: {len(changes)} fix(es)")
            for c in changes:
                print(c)
            total += len(changes)
        else:
            print(f"[CLEAN]   {f.name}: no broken math notation found")

    print()
    if total == 0:
        print("RESULT: All files clean — no unprotected math notation found.")
    else:
        print(f"RESULT: {total} fix(es) applied across {len(tex_files)} files.")
        if dry_run:
            print("(DRY RUN — no files modified. Re-run without --dry-run to apply.)")


if __name__ == "__main__":
    main()
