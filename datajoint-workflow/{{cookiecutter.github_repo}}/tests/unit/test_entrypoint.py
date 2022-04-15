"""Tests for entrypoint function

See: https://docs.pytest.org/en/6.2.x/parametrize.html
"""

import logging

import pytest

from {{cookiecutter.__pkg_import_name}}.entrypoint import setup_logging  # noqa, isort: skip


@pytest.mark.parametrize(
    "loglevelint,loglevelstr",
    [(1, "ERROR"), (2, "WARNING"), (3, "INFO"), (4, "DEBUG")],
)
def test_setup_logging(loglevelint, loglevelstr):
    """Example test with parametrization."""

    logger = setup_logging(loglevelint, base_level="CRITICAL")
    assert logging.getLevelName(logger.level) == loglevelstr
