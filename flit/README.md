<!--
conda activate base
mamba env remove -n cookies
mamba create -yn cookies "python>=3.10" pip ipykernel
conda activate cookies
pip install -U "git+https://github.com/cookiecutter/cookiecutter"
pip install -U --force-reinstall nox pre-commit black flake8 retrocookie
mamba update -c defaults -y --all

cookiecutter -vf --directory flit -o .build --no-input .

find . -name "*.DS_Store" -type f -delete
find . -name ".ipynb_checkpoints" -type d -exec rm -rf {} +
find . -name "__pycache__" -type d -exec rm -rf {} +
-->

# Workflow Template

_Cookiecutter Template for DataJoint Workflows_, **_Joseph Burling @ DataJoint_**

This [`cookiecutter`](https://cookiecutter.readthedocs.io/en/2.0.2/) template creates a python package for workflows based on the `flit_core` build backend. This follows the new [PEP 621](https://www.python.org/dev/peps/pep-0621/) standard of using a single `pyproject.toml` config file for specifying and building python packages.

## Features

- Python package build system: `flit`
- Virtual environment: `conda`
- Documentation: `mkdocs` w/ GitHub Pages deployment
- Automation:
  - `pre-commit`: Before committing, autoformat w/ `black`, sort imports with `isort`, process notebooks for version control w/ `nbstripout`, various file fixes.
  - `pytest`: Python testing framework
  - `nox`: Automate python tasks in an isolated environment like packaging, versioning, testing
  - _GitHub Actions_: Run tests on pushes and PR's, build and deploy docs, semantic versioning, automatic tags and releases, issue templates.
- IDE: `vscode` workspace w/ recommended extensions, settings, and tasks.

TODO:

- `.devcontainer`
- docker

## Using the template

### Install `cookiecutter`

You can create a new python environment to install `cookiecutter` or use an existing environment, as long as you get `cookiecutter>=2.0.0`.

_Note:_ The example below uses `conda` to create a new environment called `cookies`, activates that environment, then uses `pip` to get the latest version.

```
conda create -yn cookies "python>=3.10" pip
conda activate cookies
pip install "git+https://github.com/cookiecutter/cookiecutter"
```

### Generate the content from the template

You can use `cookiecutter` to use a template without having to manually download or clone the repository itself. The following command will use the template from the branch called `flit`, then prompt you to fill out some entries, or press `ENTER` to accept the default values shown.

```
cookiecutter --directory flit gh:datajoint-company/dj-cookiecutter
```

> Note: cookiecutter will cache/clone this specified template repo to your user directory's ~/.cookiecutters

## Updating template content 

If you have already started working on your project and you want to overwrite existing files, 

```
cookiecutter --directory flit --overwrite-if-exists gh:datajoint-company/dj-cookiecutter
```

or to skip files that already exist, 

```
cookiecutter --directory flit --skip-if-file-exists gh:datajoint-company/dj-cookiecutter
```

If you want to regenerate the most recent version of the cookiecutter template without having to re-type the values you already specified during setup, run the script `make.sh` located here: [./{{cookiecutter.github_repo}}/scripts/cookiecutter/](./{{cookiecutter.github_repo}}/scripts/cookiecutter/make.sh). It will write the new template to a folder called `build`. 

```
cd my-template-folder/scripts/cookiecutter 
chmod +x make.sh 
# make.sh --help
./make.sh -d flit -n cookies
```

## Editing the template (optional)

The following steps are only necessary if you want to customize or add to the template's content.

### Get template content

Clone this repository: `git clone https://github.com/datajoint-company/dj-cookiecutter`

Customize the template's content in the folder named [flit/{{cookecutter.github_repo}}]('./{{cookiecutter.github_repo}}/README.md') only.

Change the values in [flit/cookiecutter.json](./cookiecutter.json). Don't edit anything that starts with an underscore `_*` or `__*`, or starting at the line `"_copy_without_render"` and below.

### Build the content from the template

Make the cookiecutter package available. 

```
cd dj-cookiecutter/flit
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
