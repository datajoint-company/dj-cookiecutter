"""Use `nox` to generate `cookiecutter` content.

with nox:
    nox
    nox -s cookiecutter -- --config-file

without nox:
    cookiecutter -f -o build .
    cookiecutter --config-file cookiecutterc.yml -fv --no-input -o build .
"""

import shutil

import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["cookiecutter"]


@nox.session(python="3.10")
def update_precommit_hooks(session: nox.Session) -> None:
    """Run pre-commit autoupdate.

    nox -s update_precommit_hooks
    """

    session.install("pre-commit")
    session.run("pre-commit", "install")
    session.run(
        "pre-commit",
        "autoupdate",
        "-c",
        "{{cookiecutter.github_repo}}/.pre-commit-config.yaml",
    )


@nox.session(python="3.10")
def cookiecutter(session: nox.Session) -> None:
    """Build cookiecutter template.

    nox -s cookiecutter -- --config-file
    """

    shutil.rmtree("./build", ignore_errors=True)
    cmd_args = ["cookiecutter", "-f", "--no-input", "-o", "build"]
    sess_args = session.posargs
    if sess_args and "--config-file" in sess_args:
        cmd_args.extend(["--config-file", "cookiecutterc.yml"])

    session.install("git+https://github.com/cookiecutter/cookiecutter")
    session.run(*cmd_args, ".")
