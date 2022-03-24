_View the latest documentation site here:_ [{{cookiecutter.docs_url}}]({{cookiecutter.docs_url}}).

<!--intro-start-->

# `{{cookiecutter.__project_name}}`

_A DataJoint SciOps Workflow for {{cookiecutter.organization}}, {{cookiecutter.lab}}_

## Description

Welcome to the [_modality type_] SciOps service!

This service is designed for a user to upload their raw [_modality type_] data acquired with [_description_], which will then be automatically processed with [_..._]. The service also provides online Jupyter notebooks to visualize the results.

This [workflow](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.github_repo}}) uses components from open-source packages, including the DataJoint Elements: 

- element and url
- element and url

Please follow the steps listed below to begin working with the platform.


## Using the SciOps Services

### Account Setup

1. Create a free account at [accounts.datajoint.io](https://accounts.datajoint.io/signup)

2. Create a free GitHub account at [github.com](https://github.com/signup)

!!! attention
    Please email us at [support@datajoint.com](mailto:support@datajoint.com) after you create these accounts so we can ensure your service is configured properly.


### Data Upload 

... 

### Jupyterhub 

... 

### SciViz 

...

<!--intro-end-->
<!--install-start-->

Thank you for using the DataJoint SciOps cloud-based platform.

## Installation

!!! note
    The following is intended for developers and is not required for users of the SciOps services. 

### 1. Clone the repository

First, clone a local copy of the [project repository](https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.github_repo}}) and change to the location of that directory:

```bash
git clone https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.github_repo}}.git
cd "{{cookiecutter.__project_name}}"
```

### 2. Create a new python environment

We recommend creating an isolated [virtual environment](https://realpython.com/python-virtual-environments-a-primer/) to avoid any conflicts with your existing Python packages or interpreter. You can create a virtual environment by first installing [`conda`/`mamba`](https://github.com/conda-forge/miniforge#mambaforge):

1. Create an environment using the packages listed in `environment.yml`:

```bash
mamba env create -f environment.yml --force
```

2. Activate the new environment:

```bash
conda activate {{cookiecutter.__pkg_import_name}}
```

### 3. Install the package `{{cookiecutter.__project_name}}`

After the new virtual environment has been created and activated, install this python package using `flit` (`flit` is already in the list of requirements from the `environment.yml` file).

To avoid installing other additional packages, use the following command (see [_contrib_](./CONTRIBUTING.md#setting-up-a-local-development-environment) for extra installing packages):

```bash
flit install -s --deps=production
```

!!! note "Develop Mode Installs"
    The command `conda list` will show `{{cookiecutter.__project_name}}`, but it will be installed in _editable/develop mode_ due to using the `-s` option during installation. This means that changes will be immediately reflected when the module is reloaded.

!!! tip "Windows Links"
    This command may work better on Windows machines instead of symlinks for _develop_ mode: `flit install --pth-file --deps=production`.

If you need to uninstall the package, do so with `pip`:

```bash
pip uninstall {{cookiecutter.__project_name}}
```

#### Additional setup for local development and testing

See the [_Development setup_](./CONTRIBUTING.md#setting-up-a-local-development-environment) documentation for information on how to install additional packages and tools for local development and testing environments.

<!--install-end-->
<!--rest-of-doc-start-->

## Project Organization

```
├── .github                 <- GitHub workflows, templates, and actions.
├── data
│   ├── external            <- Data from third party sources.
│   ├── interim             <- Intermediate data that has been transformed.
│   ├── processed           <- The final, canonical data sets for modeling/plots.
│   └── raw                 <- Any original, immutable data files/dumps.
├── docker                  <- Docker image content
├── docs                    <- Directory for MkDocs documentation for gh-pages.
├── figures                 <- Generated plots and figures for reports or documentation.
├── notebooks               <- Jupyter notebooks. Naming convention is a number for
│                              ordering, the creator's initials, and a description.
|                              For example, '1.0-fw-initial-data-exploration'.
├── scripts                 <- Analysis examples or production scripts which import the
│                              actual Python package, e.g. running queries.
├── src
│   └── {{cookiecutter.__pkg_import_name}}          <- Actual Python package where the main functionality goes.
├── tests                   <- Unit tests which can be run with `pytest` or `nox`.
├── .cookiecutter.json      <- Options specified during template generation.
├── .gitignore              <- Files and folders to ignore for git.
├── .pre-commit-config.yaml <- Configuration of pre-commit git hooks.
├── CHANGELOG.md            <- Changelog to keep track of new features and fixes.
├── CONTRIBUTING.md         <- Documentation on how to contribute to the project.
├── *.code-workspace        <- Visual Studio Code workspace file.
├── {{cookiecutter._djconfig}}      <- DataJoint configuration file.
├── environment.yml         <- The conda environment file for new virtual environments.
├── LICENSE                 <- Open source license.
├── mkdocs.yml              <- Configuration for building the documentation with MkDocs.
├── noxfile.py              <- `nox` automation file for continuous integration steps.
├── pyproject.toml          <- Build system configuration for the project.
|                              Only edit if absolutely necessary.
└── README.md               <- The top-level README for the repository.
```

<!--rest-of-doc-end-->
