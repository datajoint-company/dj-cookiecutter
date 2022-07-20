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


def load_pyproject_toml(toml_file="pyproject.toml"):
    try:
        import tomli
    except ModuleNotFoundError as err:
        print(
            f"Need 'tomli' package for loading and writing TOML files '{toml_file}'",
            "\n>",
            err,
        )
        return None
    with open(toml_file, "rb") as tml:
        return tomli.load(tml)


def load_environment_yml(yaml_file="environment.yml"):
    try:
        import yaml
    except ModuleNotFoundError as err:
        print(f"Need 'pyyaml' package for loading '{yaml_file}'", "\n>", err)
        return None
    with open(yaml_file, "r") as yml:
        return yaml.safe_load(yml)


def split_deps(deps, to_move=None):
    if isinstance(to_move, str):
        to_move = [to_move]
    if not to_move:
        return deps, set()
    regex = re.compile("|".join([f"^{req}" for req in to_move]))
    to_pip = {req for req in deps if regex.match(req)}
    to_conda = set(deps) - to_pip
    return to_conda, to_pip


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


def make_devcontainer_req(requires_pip=None):
    pyproject = load_pyproject_toml()
    if not pyproject:
        return

    conda_deps, pip_deps = split_deps(
        pyproject["project"]["dependencies"], requires_pip
    )
    pip_deps = {*pip_deps, *pyproject["project"]["optional-dependencies"]["sciops"]}

    with open(
        "docker/{{cookiecutter.__pkg_import_name}}_local/.devcontainer/build/"
        "requirements/conda_requirements.txt",
        "a",
    ) as txt:
        txt.write("\n".join(sorted(conda_deps)) + "\n")

    with open(
        "docker/{{cookiecutter.__pkg_import_name}}_local/.devcontainer/build/"
        "requirements/pip_requirements.txt",
        "a",
    ) as txt:
        txt.write("\n".join(sorted(pip_deps)) + "\n")


def make_conda_env_yml(requires_pip=None):
    pyproject = load_pyproject_toml()
    conda_env = load_environment_yml()
    if not pyproject or not conda_env:
        return

    conda_deps, pip_deps = split_deps(
        pyproject["project"]["dependencies"], requires_pip
    )
    pip_deps = {*pip_deps, *pyproject["project"]["optional-dependencies"]["sciops"]}

    conda_env_dep = [i for i in conda_env.get("dependencies", []) if isinstance(i, str)]
    conda_env_pip = [
        i.get("pip", [])
        for i in conda_env.get("dependencies", [])
        if isinstance(i, dict) and "pip" in i
    ]
    conda_env_pip = conda_env_pip[0] if conda_env_pip else []
    conda_env_dep.extend(conda_deps)
    conda_env_dep = sorted(set(conda_env_dep))
    conda_env_pip.extend(pip_deps)
    conda_env_dep.append({"pip": sorted(set(conda_env_pip))})
    conda_env["dependencies"] = conda_env_dep

    import yaml

    with open("environment.yml", "w") as yml:
        yaml.dump(conda_env, yml, indent=2)


if __name__ == "__main__":
    delete_version_files()
    update_dot_cookiecutter_json()
    requires_pip = ["datajoint", "datajoint-utilities", "djsciops"]
    make_conda_env_yml(requires_pip)
    make_devcontainer_req(requires_pip)
