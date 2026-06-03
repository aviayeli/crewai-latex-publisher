import subprocess
import uuid

import pytest

from src.config import settings
from src.tools.python_runner import ALLOWED_IMPORTS, python_runner_tool


def test_tool_name_attribute():
    assert python_runner_tool.name == "python_runner"


def test_import_whitelist_is_frozenset():
    assert type(ALLOWED_IMPORTS) is frozenset


def test_valid_simple_script_executes():
    result = python_runner_tool._run(script='print("hello")')
    assert "hello" in result


def test_script_stdout_captured():
    unique = str(uuid.uuid4())
    result = python_runner_tool._run(script=f'print("{unique}")')
    assert unique in result


def test_valid_matplotlib_script_produces_png(tmp_output_dir):
    png_path = tmp_output_dir / "assets" / "test.png"
    script = (
        "import matplotlib.pyplot as plt\n"
        "import numpy as np\n"
        "plt.plot([1, 2, 3])\n"
        f'plt.savefig("{png_path}", dpi=100, bbox_inches="tight")\n'
    )
    python_runner_tool._run(script=script)
    assert png_path.exists()


def test_disallowed_import_subprocess_rejected():
    with pytest.raises(ValueError):
        python_runner_tool._run(script="import subprocess")


def test_disallowed_import_sys_rejected():
    with pytest.raises(ValueError):
        python_runner_tool._run(script="import sys")


def test_disallowed_import_shutil_rejected():
    with pytest.raises(ValueError):
        python_runner_tool._run(script="import shutil")


def test_disallowed_import_requests_rejected():
    with pytest.raises(ValueError):
        python_runner_tool._run(script="import requests")


def test_ast_scan_catches_from_import_disallowed_module():
    with pytest.raises(ValueError):
        python_runner_tool._run(script="from requests import get")


def test_allowed_import_numpy_passes_scan():
    assert python_runner_tool._scan_imports("import numpy") == []


def test_allowed_import_pathlib_passes_scan():
    assert python_runner_tool._scan_imports("from pathlib import Path") == []


def test_allowed_import_os_passes_scan():
    assert python_runner_tool._scan_imports("import os") == []


def test_scan_detects_multiple_bad_imports():
    with pytest.raises(ValueError) as exc_info:
        python_runner_tool._run(script="import subprocess\nimport requests")
    msg = str(exc_info.value)
    assert "subprocess" in msg
    assert "requests" in msg


def test_timeout_enforced(monkeypatch):
    monkeypatch.setattr(settings, "PYTHON_RUNNER_TIMEOUT_S", 1)
    with pytest.raises(subprocess.TimeoutExpired):
        python_runner_tool._run(script="while True: pass")


def test_syntax_error_reported():
    result = python_runner_tool._run(script="def foo(:")
    assert isinstance(result, str)
    assert len(result) > 0
