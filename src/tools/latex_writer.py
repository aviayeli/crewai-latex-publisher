"""CrewAI tool for writing or appending content to files in the output directory."""

from pathlib import Path
from typing import Literal

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.config import settings


class LatexWriterInput(BaseModel):
    """Input schema for the latex_writer tool."""

    path: str = Field(description="Relative path under OUTPUT_DIR or ../templates/")
    content: str = Field(description="The text to write")
    mode: Literal["write", "append", "prepend"] = Field(
        description=(
            "'write' to create/overwrite, 'append' to extend,"
            " 'prepend' to insert before existing content"
        )
    )


class LatexWriterTool(BaseTool):
    """Writes or appends text to a file inside the configured output directory."""

    name: str = "latex_writer"
    description: str = (
        "PURPOSE: Write or append text to a file inside"
        " the LaTeX output directory.\n"
        "WHEN: Any agent needs to create or extend"
        " a .tex, .md, .bib, or .json file.\n"
        "ERR: Path traversal outside OUTPUT_DIR → ValueError;"
        " mkdir failure → OSError.\n"
        "TAGS: file, write, append, tex, latex, bib, output"
    )
    args_schema: type[BaseModel] = LatexWriterInput

    def _validate_path(self, path: str) -> Path:
        """Resolve path; allow OUTPUT_DIR and TEMPLATES_DIR, reject everything else."""
        output_dir = Path(settings.OUTPUT_DIR).resolve()
        resolved = (output_dir / path).resolve()
        if resolved.is_relative_to(output_dir):
            return resolved
        templates_dir = Path(settings.TEMPLATES_DIR).resolve()
        if resolved.is_relative_to(templates_dir):
            return resolved
        raise ValueError(f"Path {path!r} escapes the allowed directories")

    def _run(self, path: str, content: str, mode: str) -> str:
        """Write, append, or prepend *content* to *path*; return confirmation."""
        resolved = self._validate_path(path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        if mode == "prepend":
            existing = resolved.read_text(encoding="utf-8") if resolved.exists() else ""
            with open(resolved, "w", encoding="utf-8") as fh:
                fh.write(content + existing)
        else:
            file_mode = "w" if mode == "write" else "a"
            with open(resolved, file_mode, encoding="utf-8") as fh:
                fh.write(content)
        return f"Written: {resolved}"


latex_writer_tool = LatexWriterTool()
