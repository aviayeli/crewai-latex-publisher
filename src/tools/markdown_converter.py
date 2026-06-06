"""CrewAI tool for converting Markdown files to LaTeX via pandoc."""

import re
import subprocess
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel

from src.config import settings


class MarkdownConverterInput(BaseModel):
    """Input schema for the markdown_converter tool."""

    md_path: str
    tex_path: str


class MarkdownConverterTool(BaseTool):
    """Converts a Markdown file to LaTeX using pandoc with raw_tex passthrough."""

    name: str = "markdown_converter"
    description: str = (
        "PURPOSE: Convert a Markdown chapter file to a LaTeX fragment via pandoc.\n"
        "WHEN: Content agent has finished a .md chapter and must produce the .tex input.\n"
        "ERR: Pandoc non-zero exit → CalledProcessError; path traversal → ValueError.\n"
        "TAGS: pandoc, markdown, latex, convert, BiDi, RTL, chapter"
    )
    args_schema: type[BaseModel] = MarkdownConverterInput

    def _validate_path(self, path: str) -> Path:
        """Resolve *path* and raise ValueError if it escapes OUTPUT_DIR."""
        output_dir = Path(settings.OUTPUT_DIR).resolve()
        resolved = (output_dir / path).resolve()
        if not resolved.is_relative_to(output_dir):
            raise ValueError(f"Path {path!r} escapes the output directory")
        return resolved

    # Pandoc escapes \textenglish{X} in two ways depending on context:
    #   code span  → \texttt{\textbackslash{}textenglish\{X\}}
    #   \\textenglish in plain text → \textbackslash textenglish\{X\}
    # Both patterns must be restored to raw \textenglish{X} so LaTeX renders
    # the command instead of printing it literally.
    _TEXTENGLISH_PATTERNS = [
        (
            re.compile(r"\\texttt\{\\textbackslash\{\}textenglish\\{([^}\\]*)\\}\}"),
            r"\\textenglish{\1}",
        ),
        (
            re.compile(r"\\textbackslash\s+textenglish\\{([^}\\]*)\\}"),
            r"\\textenglish{\1}",
        ),
    ]

    def _post_process(self, tex_path: Path) -> None:
        """Strip preamble noise and restore escaped \\textenglish{} commands.

        1. Removes \\providecommand / \\setlength / \\hypertarget lines pandoc
           adds in non-standalone mode; they collide with main.tex preamble.
        2. Unescapes \\textenglish{} that pandoc mangled inside code spans or
           when the markdown source used a double backslash.
        """
        if not tex_path.exists():
            return
        text = tex_path.read_text(encoding="utf-8")
        lines = [
            ln for ln in text.splitlines()
            if not ln.startswith((
                r"\providecommand",
                r"\setlength",
                r"\hypertarget",
            ))
        ]
        text = "\n".join(lines) + "\n"
        for pattern, replacement in self._TEXTENGLISH_PATTERNS:
            text = pattern.sub(replacement, text)
        tex_path.write_text(text, encoding="utf-8")

    def _run(self, md_path: str, tex_path: str) -> str:
        """Convert *md_path* to *tex_path* via pandoc and return a status string.

        Flags used:
          markdown+raw_tex  — inline LaTeX (\\textenglish{}, \\cite{}, etc.) passes
                              through unchanged, preserving all BiDi-safe commands.
          --wrap=none       — disables pandoc line-wrapping so Hebrew Unicode
                              codepoints are never split across lines.
        RTL rendering is handled by ``\\setmainlanguage{hebrew}`` in main.tex;
        no pandoc-level RTL flag is needed for fragment (non-standalone) output.
        """
        resolved_md = self._validate_path(md_path)
        resolved_tex = self._validate_path(tex_path)
        cmd = [
            settings.PANDOC_BIN,
            "-f", "markdown+raw_tex",
            "-t", "latex",
            "--wrap=none",
            "-o", str(resolved_tex),
            str(resolved_md),
        ]
        subprocess.run(cmd, check=True)
        self._post_process(resolved_tex)
        return f"Converted: {resolved_tex}"


markdown_converter_tool = MarkdownConverterTool()
