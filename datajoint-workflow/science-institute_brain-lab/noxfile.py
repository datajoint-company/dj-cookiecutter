"""Nox sessions.

- https://nox.thea.codes/en/stable/tutorial.html
- https://github.com/excitedleigh/setup-nox
"""

import argparse
import re

import nox

nox.options.error_on_missing_interpreters = True
nox.options.reuse_existing_virtualenvs = False
nox.options.sessions = ["write_version", "docs", "pytest"]
nox.options.pythons = ["3.9"]


def install_dependencies(session: nox.Session, *extras: str) -> None:
    session.install("setuptools>=62.0", "wheel>=0.37")
    extras = extras or ("test",)
    session.run("pip", "install", f".[{','.join(extras)}]")


def parse_session_posargs(args: list[str]) -> argparse.Namespace:
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
        "--index_html",
        dest="index_html",
        help="Add index.html to gh-page branch using mike.",
        action="store_true",
    )
    parsed_args: argparse.Namespace = parser.parse_args(args)
    return parsed_args


def git_action_bot(
    session: nox.Session, add: list[str] = None, commit: str = None, push: bool = False
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
        session.run("git", "add", "--force", *add, external=True)

    if commit is not None:
        session.log("Committing changes to remote.")
        session.run("git", "commit", "-m", commit, external=True)

    if push:
        session.log("Pushing the new changes.")
        session.run("git", "push", external=True)


@nox.session(python=nox.options.pythons[0])
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

    with open("src/brainwf/version.py", "w") as out:
        session.run("echo", f'__version__ = "{version}"', stdout=out, external=True)

    git_action_bot(session, add=["src/brainwf/version.py"])


@nox.session(python=nox.options.pythons[0])
def docs(session: nox.Session) -> None:
    """Build the latest documentation w/ mkdocs and mike.

    nox -s docs -- --version v0.0
    """

    args: argparse.Namespace = parse_session_posargs(session.posargs)
    docs_version: str = args.version.pop()
    docs_alias: str = "latest"
    index_html: bool = args.index_html

    ver_regex: re.Pattern = re.compile(
        r"^(?P<tag>v?)"
        r"(?P<major>[0-9]+)\."
        r"(?P<minor>[0-9]+)\."
        r"(?P<patch>[0-9]+.*)?"
    )
    ver_match = ver_regex.search(docs_version)
    if ver_match is None:
        docs_version = "unknown"
        docs_alias = "unknown"
    else:
        ver_groups = ver_match.groupdict()
        docs_version = f'{ver_groups["major"]}.{ver_groups["minor"]}'

    session.log(f"docs version: '{docs_version}'")
    install_dependencies(session, "doc")
    git_action_bot(session)

    session.run(
        "mike",
        "deploy",
        "--push",
        "--update-aliases",
        "-m",
        f"docs(gh-pages): build versioned documention {docs_version}:{docs_alias}",
        "-t",
        f"ver. {docs_version}",
        docs_version,
        docs_alias,
    )

    if index_html:
        session.run("mike", "set-default", "--push", "latest")


@nox.session(python=nox.options.pythons)
def pytest(session: nox.Session) -> None:
    """Run tests using pytest.

    nox -s pytest
    """

    install_dependencies(session, "test", "sciops")
    session.run("pytest")


@nox.session(python=nox.options.pythons[0])
def docs_no_ver(session: nox.Session) -> None:
    """Build the documentation w/ mkdocs.

    nox -s docs_no_ver
    """

    install_dependencies(session, "doc")
    session.run("mkdocs", "build")
