"""Module-level command-line interface

This serves as an example command-line interface for the main package module.

Example:
    Usage as a console entrypoint:

        sciops_brain_lab --help
        sciops_brain_lab --version

    Usage as a script:

        python -m sciops_brain_lab

    Usage from python:

        from sciops_brain_lab import main; main(...)
"""

import argparse
import sys
from typing import Any, Sequence

from sciops_brain_lab import version


def parse_args(args: Sequence[str]) -> argparse.Namespace:
    """_Parse command line parameters_

    Args:
        args (list[str]):
            Command line parameters as list of strings.
            (example  `["--help"]`)

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
        prog="sciops_brain_lab",
        epilog=__doc__,
        formatter_class=ArgumentDefaultsRawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s v{version}",
    )

    parsed_args = parser.parse_args(args)

    return parsed_args


def main(**kwargs: Any) -> None:
    """_Operate on cli args_."""
    print("main module operations here.")


def cli() -> None:
    """_Calls [`__main__.main`][sciops_brain_lab.__main__.main], passing the cli
    arguments extracted from `sys.argv`_.

    This function can be used as entry point to create console scripts on package
    install.
    """

    args = parse_args(sys.argv[1:])
    main(**vars(args))


if __name__ == "__main__":
    cli()
