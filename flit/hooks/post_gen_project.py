"""Hook is run after cookiecutter is done."""

import os


def delete_version_files():
    version = "{{cookiecutter.pkg_version}}"
    if not version:
        os.remove("src/{{cookiecutter.__pkg_import_name}}/version.py")


if __name__ == "__main__":
    delete_version_files()
    print("Package Name: '{{cookiecutter.__project_name}}'")
    print("Package Description: 'A DataJoint SciOps Workflow for",
          "{{cookiecutter.organization}}, {{cookiecutter.lab}}'")
    print("Package Qualified Name: '{{cookiecutter.__pkg_import_name}}'")
    print("GitHub URL: '{{cookiecutter.__github_url}}'")
