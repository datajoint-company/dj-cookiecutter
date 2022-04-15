"""Hook is run after cookiecutter is done."""

import json
import os
import re
from pathlib import Path

_CC_JSON_FILE = Path(".cookiecutter.json")


def read_dot_cc_json():
    if not _CC_JSON_FILE.exists():
        return {}

    with open(_CC_JSON_FILE, "r") as jc_file:
        json_object = json.load(jc_file)

    return json_object


def delete_version_files():
    version = "{{cookiecutter._pkg_version}}"
    if not version:
        os.remove("src/{{cookiecutter.__pkg_import_name}}/version.py")


def make_cookiecutterc_yml():
    json_object = read_dot_cc_json()
    if not json_object:
        return

    # match keys that don't start with _ or __
    negrex = re.compile(r"^_{1,2}?")
    yml_dict = {
        "default_context": {
            k: v for k, v in json_object.items() if not negrex.match(k)
        },
        "abbreviations": {
            "djcc": "https://github.com/datajoint-company/dj-cookiecutter.git"
        },
    }

    print("\nCookiecutter Context:")
    [print(f"  {k}: {v}") for k, v in yml_dict["default_context"].items()]

    out_path = Path("configs") / "cookiecutterc.yml"

    try:
        import yaml

    except ModuleNotFoundError as err:
        print(f"Need 'yaml' package for creating '{out_path}'", "\n>", err)
        return

    with open(out_path, "w") as yml_file:
        yaml.dump(yml_dict, yml_file, indent=2)


def update_dot_cookiecutter_json(remove_keys=None):
    json_object = read_dot_cc_json()
    if not json_object:
        return

    remove_keys = [] if remove_keys is None else [*remove_keys]
    remove_keys.extend(["_new_lines", "_output_dir", "_template", "_extensions"])

    json_object = {k: v for k, v in json_object.items() if k not in remove_keys}
    with open(_CC_JSON_FILE, "w") as jc_file:
        jc_file.write(json.dumps(json_object, indent=4))
        jc_file.write("\n")


def make_conda_env_yml():
    try:
        import tomli

    except ModuleNotFoundError as err:
        print("Need 'tomli' package for creating conda's environment.yml", "\n>", err)
        return

    with open("pyproject.toml", "rb") as tml:
        pyproject = tomli.load(tml)

    main_deps = pyproject["project"]["dependencies"]
    main_deps = "\n".join([f"  - {dep}" for dep in main_deps])
    sciops_deps = pyproject["project"]["optional-dependencies"]["sciops"]
    sciops_deps = "\n".join([f"      - {dep}" for dep in sciops_deps])

    with open("environment.yml", "a") as env:
        env.write(
            "  # Added from 'pyproject.toml' > " f"'.project.dependencies'\n{main_deps}"
        )
        env.write(
            "\n  # Added from 'pyproject.toml' > "
            "'.project.optional-dependencies.sciops'"
            f"\n  - pip:\n{sciops_deps}\n"
        )


if __name__ == "__main__":
    delete_version_files()
    make_cookiecutterc_yml()
    update_dot_cookiecutter_json()
    make_conda_env_yml()
