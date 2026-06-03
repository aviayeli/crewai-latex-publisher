"""CrewAI tool for writing or appending content to files in the output directory."""

from pathlib import Path
from typing import Literal

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.config import settings


class LatexWriterInput(BaseModel):
    """Input schema for the latex_writer tool."""

    path: str = Field(description="Relative path under OUTPUT_DIR")
    content: str = Field(description="The text to write")
    mode: Literal["write", "append"] = Field(
        description="'write' to create/overwrite, 'append' to extend"
    )


class LatexWriterTool(BaseTool):
    """Writes or appends text to a file inside the configured output directory."""

    name: str = "latex_writer"
    description: str = (
        "Writes or appends LaTeX content to a file inside the output directory."
    )
    args_schema: type[BaseModel] = LatexWriterInput

    def _validate_path(self, path: str) -> Path:
        """Resolve path and reject any traversal outside OUTPUT_DIR."""
        output_dir = Path(settings.OUTPUT_DIR).resolve()
        resolved = (output_dir / path).resolve()
        if not resolved.is_relative_to(output_dir):
            raise ValueError(f"Path {path!r} escapes the output directory")
        return resolved

    def _run(self, path: str, content: str, mode: str) -> str:
        """Write or append *content* to *path* and return a confirmation string."""
        resolved = self._validate_path(path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        file_mode = "w" if mode == "write" else "a"
        with open(resolved, file_mode, encoding="utf-8") as fh:
            fh.write(content)
        return f"Written: {resolved}"


latex_writer_tool = LatexWriterTool()
