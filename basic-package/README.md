# Basic Python Package Template

_Cookiecutter Template for Basic Python Packages_

This [`cookiecutter`](https://cookiecutter.readthedocs.io/en/2.0.2/) template creates a python package based on the latest `setuptools` build backend. This follows the new [PEP 621](https://www.python.org/dev/peps/pep-0621/) standard of using a single `pyproject.toml` config file for specifying and building python packages.

## Features

- Python package build system: `setuptools>=62.0`
- Virtual environment: `conda`
- Automation:
  - `pre-commit`: Before committing:
    - Autoformat w/ `black`
    - Sort imports with `isort`
    - Process notebooks for version control w/ `nbstripout`
    - Various file fixes
  - `pytest`: Python testing framework
  - `nox`: Automate python tasks in an isolated environment like packaging, versioning, testing
  - `GitHub Actions`: 
    - Run tests on pushes and PR's
    - GitHub issue templates
- IDE: 
  - `vscode` 
    - `code-workspace` Workspace file w/ recommended extensions, settings, and tasks.

## Using the template

### 1. Install `cookiecutter`

You can create a new python environment to install `cookiecutter` or use an existing environment, as long as you get `cookiecutter>=2.0.0`.

> **Note**: The example below uses `conda` to create a new environment called `cookies`, activates that environment, then uses `pip` to get the latest version.

```
conda create -yn cookies "python>=3.10" pip tomli pyyaml
conda activate cookies
pip install "git+https://github.com/cookiecutter/cookiecutter"
```

### 2. Generate the content from the template

You can use `cookiecutter` to use a template without having to manually download or clone the repository itself. The following command will use the template from the directory called `basic-package`, then prompt you to fill out some entries, or press `ENTER` to accept the default values shown.

```
cookiecutter --directory basic-package gh:datajoint-company/dj-cookiecutter
```

> Note: cookiecutter will cache/clone this specified template repo to your user directory's ~/.cookiecutters

## Updating template content 

If you have already started working on your project and you want to overwrite existing files, 

```
cookiecutter --directory basic-package --overwrite-if-exists gh:datajoint-company/dj-cookiecutter
```

or to skip files that already exist, 

```
cookiecutter --directory basic-package --skip-if-file-exists gh:datajoint-company/dj-cookiecutter
```

If you want to regenerate the most recent version of the cookiecutter template without having to re-type the values you already specified during setup, run the script [`replay.sh`](../scripts/replay/README.md).

## Editing the template (optional)

The following steps are only necessary if you want to customize or add to the template's content.

### Get template content

Clone this repository: `git clone https://github.com/datajoint-company/dj-cookiecutter`

Customize the template's content in the folder named [basic-package/{{cookecutter.github_repo}}](./{{cookiecutter.github_repo}}/README.md) only.

Change the values in [basic-package/cookiecutter.json](./cookiecutter.json). Don't edit anything that starts with an underscore `_*` or `__*`, or starting at the line `"_copy_without_render"` and below unless you know what they are for.

### Build the content from the template

Make the cookiecutter package available. 

```
cd dj-cookiecutter/basic-package
conda activate cookies
```

Build with prompts, 

```
cookiecutter -f .
```

or use the default values you specified, 

```
cookiecutter -vf --no-input .
```

### Adding back to a template

See [`retrocookie.sh`](../scripts/retrocookie/README.md) for more information.
