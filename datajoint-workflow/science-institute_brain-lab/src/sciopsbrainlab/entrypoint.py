"""Entrypoint for ingestion routines

This serves as an example command-line entrypoint for running different DataJoint
populate functions for data ingestion. Requires a valid connection to a database. The
script will run the [`run()`][sciopsbrainlab.entrypoint.run] function in this module and
requires content from the `sciopsbrainlab` package.

Example:
    Usage as a console entrypoint:

        sciopsbrainlab_entrypoint --help
        sciopsbrainlab_entrypoint task1
        sciopsbrainlab_entrypoint task2 -d 600 -s 60
        sciopsbrainlab_entrypoint -vvv task1

    Usage as a script:

        python entrypoint.py --help


    Usage from python:

        from sciopsbrainlab_entrypoint import run
        run(task=..., duration=20, sleep=5)

Attributes:
    LOGGER (logging.Logger): Module level logger when specifying verbosity.
"""

import argparse
import logging
import sys
from typing import Any, Sequence

import datajoint as dj

LOGGER: logging.Logger = logging.getLogger(__name__)


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

    class MultiplyArg(argparse.Action):
        """Custom action to multiply value of user arg"""

        def __init__(self, option_strings, multiplier=1, *args, **kwargs):
            self.mult = multiplier
            super(MultiplyArg, self).__init__(
                option_strings=option_strings, *args, **kwargs
            )

        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, self.mult * values if values > 0 else values)

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=ArgumentDefaultsRawDescriptionHelpFormatter
    )

    parser.add_argument(
        "task",
        help="The type of task/job to execute.",
        type=str,
        choices=["task1", "task2", "task3"],
    )

    parser.add_argument(
        "-d",
        "--duration",
        dest="run_duration",
        help="Specify the length of time for which to run the task (in hours)."
        "A negative duration will run in an infinite loop.",
        type=float,
        default=-1,
        action=MultiplyArg,
        multiplier=3600,
    )

    parser.add_argument(
        "-s",
        "--sleep",
        dest="sleep_duration",
        help="Time to sleep in between loops (in minutes)",
        type=float,
        default=1,
        action=MultiplyArg,
        multiplier=60,
    )

    parser.add_argument(
        "-b",
        "--backtrack",
        dest="backtrack_days",
        help="The number of days in the past for which to compare records.",
        type=int,
        default=3,
    )

    parser.add_argument(
        "-x",
        "--xtable",
        dest="exclude_tables",
        help="Exclude a behavior table. Can be used multiple times.",
        nargs="+",
        type=str,
        action="extend",
    )

    parser.add_argument(
        "--xplots",
        dest="exclude_plots",
        help="Exclude populating any plot from a populate routine.",
        action="store_true",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        dest="loglevel",
        help="Increase logging verbosity. Can be used up to 2 times "
        "at base level 'WARNING'.",
        action="count",
        default=0,
    )

    parsed_args = parser.parse_args(args)

    return parsed_args


def setup_logging(loglevel: int, base_level: str = "WARNING") -> logging.Logger:
    """_Setup basic logging_

    Args:
        loglevel (int): Minimum log level number for emitting messages.
        base_level (str, optional): Base log level name.
    """

    if loglevel is None or loglevel < 1:
        loglevel = logging.getLevelName(dj.config.get("loglevel", base_level))
    else:
        base_loglevel = logging.getLevelName(base_level)
        loglevel = base_loglevel - (10 * int(min(loglevel, base_loglevel / 10)))

    LOGGER.handlers = []
    LOGGER.setLevel(loglevel)
    print(f"logger set to level: '{logging.getLevelName(loglevel)}'")

    std_out_handler = logging.StreamHandler(stream=sys.stdout)
    std_out_handler.setLevel(loglevel)
    formatter = logging.Formatter(
        fmt="[%(asctime)s %(process)d %(processName)s "
        "%(levelname)s %(name)s]: %(message)s",
        datefmt="%z %Y-%m-%d %H:%M:%S",
    )
    std_out_handler.setFormatter(formatter)
    LOGGER.addHandler(std_out_handler)

    return LOGGER


def run(**kwargs: Any) -> None:
    """_Run ingestion routine depending on the configured task/job_

    See [Example][sciopsbrainlab.entrypoint] for a list of args.
    """

    setup_logging(kwargs.get("loglevel", 0))
    LOGGER.info("Starting ingestion process.")

    try:
        LOGGER.debug(f"Running task: '{kwargs['task']}'")
        # do something ...
    except Exception:
        LOGGER.exception(f"action '{kwargs['task']}' encountered an exception:")

    LOGGER.info("Ingestion process ended.")


def cli() -> None:
    """_Calls [`entrypoint.run`][sciopsbrainlab.entrypoint.run], passing the cli
    arguments extracted from `sys.argv`_.

    This function can be used as entry point to create console scripts on package
    install.
    """

    args = parse_args(sys.argv[1:])
    run(**vars(args))


if __name__ == "__main__":
    cli()
