"""Tests for MCPLatexServer schema and error-method handling."""



def _import_server():
    from src.tools.mcp_latex_server import (  # noqa: PLC0415
        MCPLatexServer,
        mcp_latex_server,
    )

    return MCPLatexServer, mcp_latex_server


# ── tools/list ────────────────────────────────────────────────────────────────


def test_tools_list_returns_jsonrpc_version():
    _, server = _import_server()
    resp = server.handle({"jsonrpc": "2.0", "method": "tools/list", "id": 1})
    assert resp["jsonrpc"] == "2.0"


def test_tools_list_returns_tool_named_markdown_to_latex():
    _, server = _import_server()
    resp = server.handle({"jsonrpc": "2.0", "method": "tools/list", "id": 1})
    names = [t["name"] for t in resp["result"]["tools"]]
    assert "markdown_to_latex" in names


def test_tools_list_preserves_request_id():
    _, server = _import_server()
    resp = server.handle({"jsonrpc": "2.0", "method": "tools/list", "id": 42})
    assert resp["id"] == 42


def test_tool_schema_has_md_path_and_tex_path_properties():
    _, server = _import_server()
    resp = server.handle({"jsonrpc": "2.0", "method": "tools/list", "id": 1})
    tool = resp["result"]["tools"][0]
    props = tool["inputSchema"]["properties"]
    assert "md_path" in props
    assert "tex_path" in props


def test_tool_schema_marks_both_fields_required():
    _, server = _import_server()
    resp = server.handle({"jsonrpc": "2.0", "method": "tools/list", "id": 1})
    tool = resp["result"]["tools"][0]
    assert set(tool["inputSchema"]["required"]) == {"md_path", "tex_path"}


# ── unknown method ────────────────────────────────────────────────────────────


def test_unknown_method_returns_error_object():
    _, server = _import_server()
    resp = server.handle({"jsonrpc": "2.0", "method": "nonexistent", "id": 5})
    assert "error" in resp


def test_unknown_method_error_code_is_32601():
    _, server = _import_server()
    resp = server.handle({"jsonrpc": "2.0", "method": "nonexistent", "id": 5})
    assert resp["error"]["code"] == -32601


# ── invalid JSON ──────────────────────────────────────────────────────────────


def test_invalid_json_string_returns_parse_error():
    _, server = _import_server()
    resp = server.handle("{bad json}")
    assert resp["error"]["code"] == -32700


def test_invalid_json_id_is_none():
    _, server = _import_server()
    resp = server.handle("{bad json}")
    assert resp["id"] is None
