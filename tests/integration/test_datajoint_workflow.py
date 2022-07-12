"""Run cookiecutter tests.

usage:
        > pytest tests
"""

from pathlib import Path

from cookiecutter.main import cookiecutter


def test_cookiecutter_defaults():
    out_dir = cookiecutter(
        ".",
        no_input=True,
        replay=None,
        overwrite_if_exists=True,
        output_dir="build",
        config_file=None,
        default_config=False,
        directory="datajoint-workflow",
        accept_hooks=True,
    )
    print(f"project dir: {out_dir}")


def test_cookiecutter_yml_config():
    this_dir = Path(__file__).parent
    config_file = this_dir / "fixtures" / "cookiecutterc_datajoint_workflow.yml"
    output_dir = Path("~/Documents/projects").expanduser()
    out_dir = cookiecutter(
        ".",
        no_input=True,
        replay=None,
        overwrite_if_exists=True,
        output_dir=output_dir.as_posix(),
        config_file=config_file.as_posix(),
        default_config=False,
        directory="datajoint-workflow",
        accept_hooks=True,
    )
    print(f"project dir: {out_dir}")


if __name__ == "__main__":
    test_cookiecutter_defaults()
    test_cookiecutter_yml_config()
