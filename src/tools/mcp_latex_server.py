"""Lightweight MCP-compatible JSON-RPC server exposing the Markdown→LaTeX converter."""

import json
from typing import Any

from src.tools.markdown_converter import markdown_converter_tool

_TOOL_NAME = "markdown_to_latex"
_TOOL_DESCRIPTION = (
    "Convert a Markdown file to LaTeX via Pandoc with BiDi-safe post-processing."
)
_TOOL_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "md_path": {
            "type": "string",
            "description": "Path to source Markdown file (relative to OUTPUT_DIR).",
        },
        "tex_path": {
            "type": "string",
            "description": "Destination LaTeX file path (relative to OUTPUT_DIR).",
        },
    },
    "required": ["md_path", "tex_path"],
}

_TOOLS: dict[str, dict] = {
    _TOOL_NAME: {
        "name": _TOOL_NAME,
        "description": _TOOL_DESCRIPTION,
        "inputSchema": _TOOL_SCHEMA,
    }
}


class MCPLatexServer:
    """JSON-RPC 2.0 handler that exposes markdown_converter as an MCP tool.

    Implements the subset of the Model Context Protocol needed for horizontal
    agent interoperability: tools/list and tools/call.
    """

    def handle(self, raw: str | dict) -> dict:
        """Parse a JSON-RPC 2.0 request and return a JSON-RPC 2.0 response."""
        if isinstance(raw, str):
            try:
                request = json.loads(raw)
            except json.JSONDecodeError as exc:
                return self._error(None, -32700, f"Parse error: {exc}")
        else:
            request = raw

        req_id = request.get("id")
        method = request.get("method", "")
        params = request.get("params", {})

        if method == "tools/list":
            return self._result(req_id, {"tools": list(_TOOLS.values())})
        if method == "tools/call":
            return self._dispatch(req_id, params)
        return self._error(req_id, -32601, f"Method not found: {method!r}")

    def _dispatch(self, req_id: Any, params: dict) -> dict:
        name = params.get("name")
        args = params.get("arguments", {})
        if name not in _TOOLS:
            return self._error(req_id, -32602, f"Unknown tool: {name!r}")
        try:
            text = markdown_converter_tool._run(**args)
            return self._result(req_id, {"content": [{"type": "text", "text": text}]})
        except (ValueError, TypeError) as exc:
            return self._error(req_id, -32602, str(exc))
        except Exception as exc:
            return self._error(req_id, -32603, f"Internal error: {exc}")

    @staticmethod
    def _result(req_id: Any, result: Any) -> dict:
        return {"jsonrpc": "2.0", "result": result, "id": req_id}

    @staticmethod
    def _error(req_id: Any, code: int, message: str) -> dict:
        return {
            "jsonrpc": "2.0",
            "error": {"code": code, "message": message},
            "id": req_id,
        }


mcp_latex_server = MCPLatexServer()
