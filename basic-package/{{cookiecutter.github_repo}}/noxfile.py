"""Nox sessions.

- https://nox.thea.codes/en/stable/tutorial.html
- https://github.com/excitedleigh/setup-nox
"""

import argparse
import os

import nox

default_python_version = "{{cookiecutter.python_version}}"
nox.options.error_on_missing_interpreters = True
nox.options.reuse_existing_virtualenvs = False
nox.options.sessions = ["write_version", "docs", "pytest"]
nox.options.pythons = [default_python_version]


def install_dependencies(session: nox.Session, *extras: str) -> None:
    session.install("setuptools>=62.0", "wheel>=0.37")
    extras = extras or ("test",)
    session.run("pip", "install", f".[{','.join(extras)}]")


def parse_session_posargs(args: list[str]) -> argparse.Namespace:
    class SplitCSA(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if values:
                setattr(namespace, self.dest, values.split(","))

    parser = argparse.ArgumentParser(description="Parse position args sent to nox.")
    parser.add_argument(
        "--version",
        dest="version",
        default=["unknown"],
        type=str,
        nargs=1,
        help="The major.minor version string.",
    )
    parser.add_argument(
        "--pversion",
        dest="prev_ver",
        default=["unknown"],
        type=str,
        nargs=1,
        help="The previous major.minor version string.",
    )
    parser.add_argument(
        "--pre-commit-hooks",
        dest="pre_commit_hooks",
        default=["black", "isort"],
        action=SplitCSA,
        help="Comma-separated names of pre-commit hooks to run.",
    )
    parser.add_argument(
        "--index_html",
        dest="index_html",
        help="Add index.html to gh-page branch using mike.",
        action="store_true",
    )
    parser.add_argument(
        "--fail",
        dest="fail",
        help="Flag to force exception on failed session run.",
        action="store_true",
    )
    parsed_args: argparse.Namespace = parser.parse_args(args)
    return parsed_args


def git_action_bot(
    session: nox.Session,
    add: list[str] = None,
    commit: list[str] = None,
    push: list[str] = None,
) -> None:
    session.log("Configuring git user and email.")
    session.run(
        "git", "config", "--local", "user.name", "github-actions[bot]", external=True
    )
    session.run(
        "git",
        "config",
        "--local",
        "user.email",
        "github-actions[bot]@users.noreply.github.com",
        external=True,
    )

    if add:
        session.log("Adding files to commit.")
        session.run("git", "add", *add, external=True)

    if commit:
        session.log("Committing changes to remote.")
        session.run("git", "commit", *commit, external=True)

    if push:
        session.log("Pushing the new changes.")
        session.run("git", "push", *push, external=True)


@nox.session(python=default_python_version, reuse_venv=True)
def main_cli(session: nox.Session) -> None:
    """Install all dependencies then run package main cli with arg '--version'.

    nox -s main_cli
    """

    install_dependencies(session, "dev", "test")
    session.run("{{cookiecutter.__pkg_import_name}}", "--version")


@nox.session(python=default_python_version, reuse_venv=True)
def write_version(session: nox.Session) -> None:
    """Bump version.py to the latest version.

    nox -s write_version -- --version 0.0.1
    """

    args: argparse.Namespace = parse_session_posargs(session.posargs)
    version: str = args.version.pop()
    prev_ver: str = args.prev_ver.pop()

    if version == prev_ver:
        session.log(f"Skipping overwriting 'version.py' to '{version}'")
        return

    session.log(f"Overwriting 'version.py' to '{version}'")

    with open("src/{{cookiecutter.__pkg_import_name}}/version.py", "w") as out:
        session.run("echo", f'__version__ = "{version}"', stdout=out, external=True)

    git_action_bot(session, add=["--force", "src/{{cookiecutter.__pkg_import_name}}/version.py"])


@nox.session(python=default_python_version, reuse_venv=True)
def pre_commit(session: nox.Session) -> None:
    """Run pre-commit.

    nox -s pre_commit -- --pre-commit-hooks=black,isort --fail
    """

    args: argparse.Namespace = parse_session_posargs(session.posargs)
    hooks: list[str] = args.pre_commit_hooks
    raise_exception: bool = args.fail

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
        failed_str = "Failed pre-commit hooks:"
        failed_str += "".join(
            [f"\n::{hk}\n\n{txt}\n" for hk, txt in failed_hooks.items()]
        )
        if raise_exception:
            session.error(failed_str)
        else:
            session.log(failed_str)


@nox.session(python=nox.options.pythons)
def pytest(session: nox.Session) -> None:
    """Run tests using pytest.

    nox -s pytest
    """

    pytest_args = session.posargs or ["tests"]
    install_dependencies(session, "test")
    session.run("pytest", *pytest_args)
