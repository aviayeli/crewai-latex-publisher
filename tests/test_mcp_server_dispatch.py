"""Tests for MCPLatexServer tools/call dispatch and singleton."""

from unittest.mock import patch


def _import_server():
    from src.tools.mcp_latex_server import (  # noqa: PLC0415
        MCPLatexServer,
        mcp_latex_server,
    )

    return MCPLatexServer, mcp_latex_server


# ── tools/call ────────────────────────────────────────────────────────────────


def test_tools_call_unknown_tool_returns_invalid_params_error():
    _, server = _import_server()
    resp = server.handle({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": "unknown_tool", "arguments": {}},
        "id": 9,
    })
    assert "error" in resp
    assert resp["error"]["code"] == -32602


def test_tools_call_dispatches_to_converter(tmp_path):
    _, server = _import_server()
    with patch("src.tools.mcp_latex_server.markdown_converter_tool._run",
               return_value="Converted: output.tex") as mock_run:
        resp = server.handle({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "markdown_to_latex",
                "arguments": {"md_path": "ch1.md", "tex_path": "ch1.tex"},
            },
            "id": 7,
        })
    mock_run.assert_called_once_with(md_path="ch1.md", tex_path="ch1.tex")
    assert resp["result"]["content"][0]["type"] == "text"


def test_tools_call_content_text_matches_converter_output():
    _, server = _import_server()
    with patch("src.tools.mcp_latex_server.markdown_converter_tool._run",
               return_value="Converted: ch2.tex"):
        resp = server.handle({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "markdown_to_latex",
                "arguments": {"md_path": "ch2.md", "tex_path": "ch2.tex"},
            },
            "id": 8,
        })
    assert resp["result"]["content"][0]["text"] == "Converted: ch2.tex"


def test_tools_call_value_error_returns_invalid_params_error():
    _, server = _import_server()
    with patch("src.tools.mcp_latex_server.markdown_converter_tool._run",
               side_effect=ValueError("escapes output dir")):
        resp = server.handle({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "markdown_to_latex",
                "arguments": {"md_path": "../../etc", "tex_path": "out.tex"},
            },
            "id": 10,
        })
    assert resp["error"]["code"] == -32602
    assert "escapes" in resp["error"]["message"]


def test_tools_call_unexpected_exception_returns_internal_error():
    _, server = _import_server()
    with patch("src.tools.mcp_latex_server.markdown_converter_tool._run",
               side_effect=RuntimeError("pandoc crashed")):
        resp = server.handle({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "markdown_to_latex",
                "arguments": {"md_path": "ch1.md", "tex_path": "ch1.tex"},
            },
            "id": 11,
        })
    assert resp["error"]["code"] == -32603


# ── dict input (pre-parsed) ───────────────────────────────────────────────────


def test_dict_input_is_accepted_without_json_parsing():
    _, server = _import_server()
    resp = server.handle({"jsonrpc": "2.0", "method": "tools/list", "id": 99})
    assert "result" in resp


# ── module-level singleton ────────────────────────────────────────────────────


def test_mcp_latex_server_singleton_is_mcp_latex_server_instance():
    MCPLatexServer, mcp_latex_server = _import_server()
    assert isinstance(mcp_latex_server, MCPLatexServer)
