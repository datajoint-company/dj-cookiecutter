"""Hook is run after cookiecutter is done."""

import json
import os
from pathlib import Path


def delete_version_files():
    version = "{{cookiecutter.pkg_version}}"
    if not version:
        os.remove("src/{{cookiecutter.__pkg_import_name}}/version.py")


def update_dot_cookiecutter_json(remove_keys=None):
    cc_file = Path(".cookiecutter.json")
    if cc_file.exists():
        remove_keys = [] if remove_keys is None else [*remove_keys]
        remove_keys.extend(["_new_lines", "_output_dir", "_template"])
        with open(cc_file, "r") as jc_file:
            json_object = json.load(jc_file)

        json_object = {k: v for k, v in json_object.items() if k not in remove_keys}
        with open(cc_file, "w") as jc_file:
            jc_file.write(json.dumps(json_object, indent=4))
            jc_file.write("\n")


def create_conda_env_yml():
    try:
        import tomli

    except:
        print("Need 'tomli' package for creating conda's environment.yml")
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
    update_dot_cookiecutter_json()
    create_conda_env_yml()
    print("Package Name: '{{cookiecutter.__project_name}}'")
    print(
        "Package Description: 'A DataJoint SciOps Workflow for",
        "{{cookiecutter.organization}}, {{cookiecutter.lab}}'",
    )
    print("Package Qualified Name: '{{cookiecutter.__pkg_import_name}}'")
    print(
        "GitHub URL: 'https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.github_repo}}'"
    )
