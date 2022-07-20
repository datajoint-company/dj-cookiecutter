# type: ignore
"""Nox sessions.

- https://nox.thea.codes/en/stable/tutorial.html
- https://github.com/excitedleigh/setup-nox
"""

import argparse
import os

import nox

default_python_version = "3.10"
nox.options.error_on_missing_interpreters = True
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["main_cli", "pre_commit", "pytest"]
nox.options.pythons = [default_python_version]


def install_dependencies(session, *extras):
    session.install("setuptools>=62.0", "wheel>=0.37")
    extras = extras or ("test",)
    session.run("pip", "install", f".[{','.join(extras)}]")


def parse_session_posargs(args):
    class SplitCSA(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if values:
                setattr(namespace, self.dest, values.split(","))

    parser = argparse.ArgumentParser(description="Parse position args sent to nox.")
    parser.add_argument(
        "--pre-commit-hooks",
        dest="pre_commit_hooks",
        default=["black", "isort"],
        action=SplitCSA,
        help="Comma-separated names of pre-commit hooks to run.",
    )
    parser.add_argument(
        "--fail",
        dest="fail",
        help="Flag to force exception on failed session run.",
        action="store_true",
    )
    parsed_args = parser.parse_args(args)
    return parsed_args


@nox.session(python=default_python_version, reuse_venv=True)
def main_cli(session):
    """Install all dependencies then run package main cli with arg '--version'.

    nox -s main_cli
    """

    install_dependencies(session, "dev", "test")
    session.run("basic_package", "--version")


@nox.session(python=default_python_version, reuse_venv=True)
def pre_commit(session):
    """Run pre-commit.

    nox -s pre_commit -- --pre-commit-hooks=black,isort --fail
    """

    args = parse_session_posargs(session.posargs)
    hooks = args.pre_commit_hooks
    raise_exception = args.fail

    install_dependencies(session, "dev")
    session.run("pre-commit", "install")

    failed_hooks = {}
    log_file = ".nox.pre-commit.log"
    for hook in hooks:
        try:
            with open(log_file, "w") as fout:
                session.run("pre-commit", "run", "--all-files", hook, stdout=fout)

        except Exception as err:
            session.log(err)
            with open(log_file, "r") as fin:
                failed_hooks[hook] = fin.read()

        finally:
            os.remove(log_file)

    if failed_hooks:
        failed_str = "Failed pre-commit hooks:" + "".join(
            [f"\n::{hk}\n\n{txt}\n" for hk, txt in failed_hooks.items()]
        )

        if raise_exception:
            session.error(failed_str)
        else:
            session.log(failed_str)


@nox.session(python=nox.options.pythons)
def pytest(session):
    """Run tests using pytest.

    nox -s pytest
    """

    pytest_args = session.posargs or ["tests"]
    install_dependencies(session, "test")
    session.run("pytest", *pytest_args)
