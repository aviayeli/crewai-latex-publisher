import subprocess
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel

from src.config import settings


class CompilationError(Exception):
    pass


class LualatexRunnerInput(BaseModel):
    tex_file: str
    passes: int = 2
    run_biber: bool = True


class LualatexRunnerTool(BaseTool):
    name: str = "lualatex_runner"
    description: str = (
        "Runs lualatex (and optionally biber) to compile a .tex file to PDF."
    )
    args_schema: type[BaseModel] = LualatexRunnerInput

    def _build_cmd(self, tex_file: str) -> list[str]:
        return [
            settings.LUALATEX_BIN,
            "--interaction=nonstopmode",
            f"--output-directory={settings.OUTPUT_DIR}",
            tex_file,
        ]

    def _build_biber_cmd(self, stem: str) -> list[str]:
        return [settings.BIBER_BIN, stem]

    def _parse_log(self, log_path: Path) -> list[str]:
        try:
            text = log_path.read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError:
            return []
        return [line for line in text.splitlines() if line.startswith("! ")]

    def _run(self, tex_file: str, passes: int = 2, run_biber: bool = True) -> dict:
        log_path = Path(settings.OUTPUT_DIR) / (Path(tex_file).stem + ".log")

        def _latex(path: str) -> None:
            try:
                subprocess.run(self._build_cmd(path), check=True)
            except subprocess.CalledProcessError:
                errors = self._parse_log(log_path)
                raise CompilationError(
                    "\n".join(errors) if errors else "lualatex exited non-zero"
                )

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
