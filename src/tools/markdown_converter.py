"""CrewAI tool for converting Markdown files to LaTeX via pandoc."""

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
    description: str = "Converts a Markdown file to LaTeX using pandoc."
    args_schema: type[BaseModel] = MarkdownConverterInput

    def _validate_path(self, path: str) -> Path:
        """Resolve *path* and raise ValueError if it escapes OUTPUT_DIR."""
        output_dir = Path(settings.OUTPUT_DIR).resolve()
        resolved = (output_dir / path).resolve()
        if not resolved.is_relative_to(output_dir):
            raise ValueError(f"Path {path!r} escapes the output directory")
        return resolved

    def _run(self, md_path: str, tex_path: str) -> str:
        """Convert *md_path* to *tex_path* via pandoc and return a status string."""
        resolved_md = self._validate_path(md_path)
        resolved_tex = self._validate_path(tex_path)
        cmd = [
            settings.PANDOC_BIN,
            "-f", "markdown+raw_tex",
            "-t", "latex",
            "-o", str(resolved_tex),
            str(resolved_md),
        ]
        subprocess.run(cmd, check=True)
        return f"Converted: {resolved_tex}"


markdown_converter_tool = MarkdownConverterTool()
