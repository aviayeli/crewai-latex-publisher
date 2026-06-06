"""Red-team: forbidden module injection via python_runner_tool."""

import pytest

from src.tools.python_runner import python_runner_tool


class TestToolMisuseBlocked:
    """Attacker passes scripts importing forbidden modules to python_runner_tool.

    Defence: PythonRunnerTool._scan_imports() — returns blocked names;
             PythonRunnerTool._run() raises ValueError on any blocked import.
    """

    def test_subprocess_import_flagged_by_scanner(self):
        script = "import subprocess; subprocess.run(['rm', '-rf', '/'])"
        bad = python_runner_tool._scan_imports(script)
        assert "subprocess" in bad

    def test_sys_import_flagged_by_scanner(self):
        bad = python_runner_tool._scan_imports("import sys; sys.exit(0)")
        assert "sys" in bad

    def test_socket_import_flagged_by_scanner(self):
        script = "import socket; socket.connect(('evil.com', 80))"
        bad = python_runner_tool._scan_imports(script)
        assert "socket" in bad

    def test_from_import_subprocess_flagged_by_scanner(self):
        script = "from subprocess import run; run(['id'])"
        bad = python_runner_tool._scan_imports(script)
        assert "subprocess" in bad

    def test_from_import_sys_module_flagged_by_scanner(self):
        bad = python_runner_tool._scan_imports("from sys import argv")
        assert "sys" in bad

    def test_chained_forbidden_imports_all_flagged(self):
        script = "import socket, subprocess, sys, shutil, ctypes"
        bad = python_runner_tool._scan_imports(script)
        assert "subprocess" in bad
        assert "socket" in bad
        assert "sys" in bad

    def test_shutil_import_flagged_by_scanner(self):
        bad = python_runner_tool._scan_imports("import shutil; shutil.rmtree('/')")
        assert "shutil" in bad

    def test_forbidden_import_raises_valueerror_on_run(self):
        with pytest.raises(ValueError, match="disallowed"):
            python_runner_tool._run("import subprocess; subprocess.run(['ls'])")

    def test_ctypes_import_flagged_by_scanner(self):
        script = "import ctypes; ctypes.cdll.LoadLibrary('evil.so')"
        bad = python_runner_tool._scan_imports(script)
        assert "ctypes" in bad

    def test_allowed_imports_produce_empty_scan_result(self):
        script = "import matplotlib\nimport numpy\nimport pathlib\nimport os"
        bad = python_runner_tool._scan_imports(script)
        assert bad == []

    def test_script_with_no_imports_is_clean(self):
        bad = python_runner_tool._scan_imports("x = 1 + 1\nprint(x)")
        assert bad == []
