"""Module-level command-line interface

This serves as an example command-line interface for the main package module.

Example:
    Usage as a package cli:

        {{cookiecutter.__pkg_import_name}} --help
        {{cookiecutter.__pkg_import_name}} --version

    Usage as a script:

        python -m {{cookiecutter.__pkg_import_name}}

    Usage from python:

        from {{cookiecutter.__pkg_import_name}} import main; main(...)
"""

import argparse
import sys
from typing import Any, Sequence

from {{cookiecutter.__pkg_import_name}} import version


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
        prog="{{cookiecutter.__pkg_import_name}}",
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
    """_Calls [`__main__.main`][{{cookiecutter.__pkg_import_name}}.__main__.main], passing the cli
    arguments extracted from `sys.argv`_.

    This function can be used as entry point to create console scripts on package
    install.
    """

    args = parse_args(sys.argv[1:])
    main(**vars(args))


if __name__ == "__main__":
    cli()
