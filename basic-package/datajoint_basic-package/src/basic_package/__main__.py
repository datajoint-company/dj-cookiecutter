"""Module-level command-line interface

This serves as an example command-line interface for the main package module.

Example:
    Usage as a package cli:

        basic_package --help
        basic_package --version

    Usage as a script:

        python -m basic_package

    Usage from python:

        from basic_package import main; main(...)
"""

import argparse
import sys
from typing import Any, Sequence

from basic_package import VERSION


def parse_args(args: Sequence[str]) -> argparse.Namespace:
    """Parse command line parameters

    Args:
        args (Sequence[str]):
            Command line parameters as list of strings (example: `["--help"]`).

    Returns:
        A Namespace of command line parameters.
    """

    class ArgumentDefaultsRawDescriptionHelpFormatter(
        argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter,
        argparse.MetavarTypeHelpFormatter,
    ):
        """Combination of different formatters"""

        pass

    parser = argparse.ArgumentParser(
        prog="basic_package",
        epilog=__doc__,
        formatter_class=ArgumentDefaultsRawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s v{VERSION}",
    )

    return parser.parse_args(args)


def main(**kwargs: Any) -> None:
    """Operate on cli args."""
    print("main module operations here.")


def cli() -> None:
    """Calls [`__main__.main`][basic_package.__main__.main], passing the cli
    arguments extracted from `sys.argv`.

    This function can be used as entry point to create console scripts on package
    install.
    """

    args = parse_args(sys.argv[1:])
    main(**vars(args))


if __name__ == "__main__":
    cli()
