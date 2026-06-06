"""CrewAI tool for sandboxed Python execution with import allowlist enforcement."""

import ast
import subprocess
import tempfile
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel

from src.config import settings

# Security invariant — not a hyperparameter; must not move to .env
ALLOWED_IMPORTS: frozenset = frozenset({"matplotlib", "numpy", "pathlib", "os"})


class PythonRunnerInput(BaseModel):
    """Input schema for the python_runner tool."""

    script: str


class PythonRunnerTool(BaseTool):
    """Executes a sandboxed Python script after scanning for disallowed imports."""

    name: str = "python_runner"
    description: str = (
        "PURPOSE: Execute a sandboxed matplotlib/numpy script"
        " and capture stdout.\n"
        "WHEN: Figure agent must generate a PNG chart from a Python script.\n"
        "ERR: Disallowed imports → ValueError; timeout → TimeoutExpired;"
        " non-zero → stderr.\n"
        "TAGS: figures, matplotlib, numpy, chart, PNG, sandbox, execute"
    )
    args_schema: type[BaseModel] = PythonRunnerInput

    def _scan_imports(self, script: str) -> list[str]:
        """Return sorted list of top-level imports not in ALLOWED_IMPORTS."""
        try:
            tree = ast.parse(script)
        except SyntaxError:
            return []
        disallowed: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    if top not in ALLOWED_IMPORTS:
                        disallowed.append(top)
            elif isinstance(node, ast.ImportFrom) and node.module:
                top = node.module.split(".")[0]
                if top not in ALLOWED_IMPORTS:
                    disallowed.append(top)
        return sorted(set(disallowed))

    def _run(self, script: str) -> str:
        """Validate imports, write to a temp file, execute, and return output."""
        bad = self._scan_imports(script)
        if bad:
            raise ValueError(f"disallowed imports: {', '.join(bad)}")
        with tempfile.NamedTemporaryFile(
            suffix=".py", mode="w", delete=False, encoding="utf-8"
        ) as tf:
            tf.write(script)
            tmpfile = tf.name
        try:
            result = subprocess.run(
                ["python3", tmpfile],
                capture_output=True,
                text=True,
                timeout=settings.PYTHON_RUNNER_TIMEOUT_S,
            )
        except subprocess.TimeoutExpired:
            raise
        finally:
            Path(tmpfile).unlink(missing_ok=True)
        return result.stdout if result.returncode == 0 else result.stderr


python_runner_tool = PythonRunnerTool()
