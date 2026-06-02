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
    script: str


class PythonRunnerTool(BaseTool):
    name: str = "python_runner"
    description: str = (
        "Executes a sandboxed Python script and returns stdout or stderr."
    )
    args_schema: type[BaseModel] = PythonRunnerInput

    def _scan_imports(self, script: str) -> list[str]:
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
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    top = node.module.split(".")[0]
                    if top not in ALLOWED_IMPORTS:
                        disallowed.append(top)
        return sorted(set(disallowed))

    def _run(self, script: str) -> str:
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
