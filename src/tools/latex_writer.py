from pathlib import Path
from typing import Literal

from crewai.tools import BaseTool
from pydantic import BaseModel

from src.config import settings


class LatexWriterInput(BaseModel):
    path: str
    content: str
    mode: Literal["write", "append"]


class LatexWriterTool(BaseTool):
    name: str = "latex_writer"
    description: str = (
        "Writes or appends LaTeX content to a file inside the output directory."
    )
    args_schema: type[BaseModel] = LatexWriterInput

    def _validate_path(self, path: str) -> Path:
        output_dir = Path(settings.OUTPUT_DIR).resolve()
        resolved = (output_dir / path).resolve()
        if not resolved.is_relative_to(output_dir):
            raise ValueError(f"Path {path!r} escapes the output directory")
        return resolved

    def _run(self, path: str, content: str, mode: str) -> str:
        resolved = self._validate_path(path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        file_mode = "w" if mode == "write" else "a"
        with open(resolved, file_mode, encoding="utf-8") as fh:
            fh.write(content)
        return f"Written: {resolved}"


latex_writer_tool = LatexWriterTool()
