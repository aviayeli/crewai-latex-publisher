"""CLI entry point — installed as ``latex-publisher`` via pyproject.toml.

All business logic is delegated to LatexPublisherSDK.
The CLI layer is intentionally thin: show menu, call SDK, print result.

Usage::

    latex-publisher run          # present topic menu and execute pipeline
    latex-publisher --version    # print package version
    latex-publisher --help       # show usage
"""

import sys

import dotenv

from src.sdk.latex_publisher_sdk import LatexPublisherSDK
from src.topics import select_topic

_USAGE = "Usage: latex-publisher [run | --version | --help]"


def main() -> None:
    """Entry point for the ``latex-publisher`` CLI command."""
    dotenv.load_dotenv()
    sdk = LatexPublisherSDK()
    args = sys.argv[1:]

    if not args or args[0] == "run":
        selected = select_topic()
        result = sdk.run(topic=selected.title, research_focus=selected.research_focus)
        print(result)
    elif args[0] in ("--version", "-v"):
        print(f"latex-publisher {sdk.version}")
    elif args[0] in ("--help", "-h"):
        print(_USAGE)
    else:
        print(f"Unknown command: {args[0]!r}", file=sys.stderr)
        print(_USAGE, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
