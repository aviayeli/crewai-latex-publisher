"""CLI entry point — installed as ``latex-publisher`` via pyproject.toml.

All business logic is delegated to LatexPublisherSDK.
The CLI layer is intentionally thin: parse argv, call SDK, print result.

Usage::

    latex-publisher run          # execute the full pipeline
    latex-publisher --version    # print package version
    latex-publisher --help       # show usage
"""

import sys

import dotenv

from src.sdk.latex_publisher_sdk import LatexPublisherSDK

_USAGE = "Usage: latex-publisher [run | --version | --help]"


def main() -> None:
    """Entry point for the ``latex-publisher`` CLI command."""
    dotenv.load_dotenv()
    sdk = LatexPublisherSDK()
    args = sys.argv[1:]

    if not args or args[0] == "run":
        topic = input(
            "Enter the topic for the agents to research and write about: "
        ).strip()
        result = sdk.run(topic=topic)
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
