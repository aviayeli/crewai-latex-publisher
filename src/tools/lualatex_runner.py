"""CrewAI tool for compiling LuaLaTeX documents with optional Biber bibliography."""

import subprocess
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel

from src.config import settings


class CompilationError(Exception):
    """Raised when lualatex or biber exits non-zero."""


class LualatexRunnerInput(BaseModel):
    """Input schema for the lualatex_runner tool."""

    tex_file: str
    passes: int = 3
    run_biber: bool = True


class LualatexRunnerTool(BaseTool):
    """Runs lualatex (and optionally biber) to compile a .tex file to PDF."""

    name: str = "lualatex_runner"
    description: str = (
        "Runs lualatex (and optionally biber) to compile a .tex file to PDF."
    )
    args_schema: type[BaseModel] = LualatexRunnerInput

    def _build_cmd(self, tex_file: str) -> list[str]:
        """Build the lualatex subprocess command list."""
        return [
            settings.LUALATEX_BIN,
            "--interaction=nonstopmode",
            f"--output-directory={settings.OUTPUT_DIR}",
            tex_file,
        ]

    def _build_biber_cmd(self, stem: str) -> list[str]:
        """Build the biber subprocess command list."""
        return [settings.BIBER_BIN, stem]

    def _parse_log(self, log_path: Path) -> list[str]:
        """Return lines starting with '!' from the lualatex log file."""
        try:
            text = log_path.read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError:
            return []
        return [line for line in text.splitlines() if line.startswith("! ")]

    def _run(
        self, tex_file: str, passes: int = 3, run_biber: bool = True
    ) -> dict:
        """Compile *tex_file*, run biber if requested, and repeat for *passes*."""
        if settings.HITL_ENABLED:
            answer = input(
                f"\n[HITL] Press Y to execute the {passes}-step PDF compilation"
                f" for '{tex_file}' [Y/n]: "
            ).strip().upper()
            if answer != "Y":
                raise RuntimeError(
                    "HITL gate: compilation cancelled by operator."
                )

        log_path = Path(settings.OUTPUT_DIR) / (Path(tex_file).stem + ".log")

        def _latex(path: str) -> None:
            try:
                subprocess.run(self._build_cmd(path), check=True)
            except subprocess.CalledProcessError as exc:
                errors = self._parse_log(log_path)
                raise CompilationError(
                    "\n".join(errors) if errors else "lualatex exited non-zero"
                ) from exc

        _latex(tex_file)

        if run_biber:
            stem = f"{settings.OUTPUT_DIR}/{Path(tex_file).stem}"
            subprocess.run(self._build_biber_cmd(stem), check=True)

        for _ in range(passes - 1):
            _latex(tex_file)

        errors = self._parse_log(log_path)
        if errors:
            raise CompilationError("\n".join(errors))

        return {"success": True}


lualatex_runner_tool = LualatexRunnerTool()
