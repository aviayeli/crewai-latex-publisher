"""Verify all CrewAI tools expose TTC-format descriptions (FinOps guardrail)."""

_TTC_FIELDS = ("PURPOSE:", "WHEN:", "ERR:", "TAGS:")


def _assert_ttc(description: str, tool_name: str) -> None:
    for field in _TTC_FIELDS:
        assert field in description, (
            f"Tool '{tool_name}' description missing TTC field '{field}'"
        )


def test_perplexity_search_has_ttc_description():
    from src.tools.perplexity_search import perplexity_search_tool
    _assert_ttc(perplexity_search_tool.description, "perplexity_search")


def test_python_runner_has_ttc_description():
    from src.tools.python_runner import python_runner_tool
    _assert_ttc(python_runner_tool.description, "python_runner")


def test_latex_writer_has_ttc_description():
    from src.tools.latex_writer import latex_writer_tool
    _assert_ttc(latex_writer_tool.description, "latex_writer")


def test_markdown_converter_has_ttc_description():
    from src.tools.markdown_converter import markdown_converter_tool
    _assert_ttc(markdown_converter_tool.description, "markdown_converter")


def test_lualatex_runner_has_ttc_description():
    from src.tools.lualatex_runner import lualatex_runner_tool
    _assert_ttc(lualatex_runner_tool.description, "lualatex_runner")


def test_mcp_tool_description_has_ttc_format():
    from src.tools.mcp_latex_server import mcp_latex_server
    resp = mcp_latex_server.handle(
        {"jsonrpc": "2.0", "method": "tools/list", "id": 1}
    )
    desc = resp["result"]["tools"][0]["description"]
    _assert_ttc(desc, "markdown_to_latex (MCP)")
