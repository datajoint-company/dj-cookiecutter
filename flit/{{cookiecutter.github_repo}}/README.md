_View the latest documentation site here:_ [{{cookiecutter.__url_documentation}}]({{cookiecutter.__url_documentation}}).

<!--intro-start-->

# `{{cookiecutter.__project_name}}`

_{{cookiecutter.__short_description}}_

## Description

Welcome to the [_modality type_] SciOps service!

This service is designed for a user to upload their raw [_modality type_] data acquired with [_description_], which will then be automatically processed with [_..._]. The service also provides online Jupyter notebooks to visualize the results.

This [workflow]({{cookiecutter.__github_url}}) uses components from open-source packages, including the DataJoint Elements: 

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

### Clone the repository

First, clone a copy of the [project repository]({{cookiecutter.__github_url}}) to your local disk and switch to that directory:

```bash
git clone {{cookiecutter.__github_url}}.git
cd "{{cookiecutter.__project_name}}"
```

### Create a new python environment

We recommend creating an isolated [virtual environment](https://realpython.com/python-virtual-environments-a-primer/) to avoid any problems with your existing Python packages and interpreter. This can be done via [Conda/Mamba](https://github.com/conda-forge/miniforge#mambaforge):

1. Create the environment using the packages specified in `environment.yml`:

```bash
mamba env create -f environment.yml --force
```

2. Activate the new environment:

```bash
conda activate {{cookiecutter.__pkg_import_name}}
```

### Install the package `{{cookiecutter.__project_name}}`

After the new virtual environment has been created and activate, install the package using `flit` (`flit` was already in the requirements from the `environment.yml` file).

Install only the necessary packages in _develop_ mode (see [_contrib_](./CONTRIBUTING.md#setting-up-a-local-development-environment) for extra packages):

```bash
flit install -s --deps=production
```

!!! note "Develop Mode Installs"
    The conda environment will have `{{cookiecutter.__pkg_import_name}}` installed in editable/develop mode. This means that changes will be immediately reflected when the module is reloaded.

!!! tip "Windows Links"
    This command may work better on Windows machines instead of symlinks for _develop_ mode: `flit install --pth-file --deps=production`.

If you need to uninstall the package, do so with `pip`:

```bash
pip uninstall {{cookiecutter.__project_name}}
rm -rf src/{{cookiecutter.__project_name}}.egg*
```

#### Setup for local development

See the [_Development setup_](./CONTRIBUTING.md#setting-up-a-local-development-environment) documentation for information on how to install additional packages and tools.

## Dependency Management & Reproducibility

1. Always keep your abstract (unpinned) dependencies updated in `environment.yml` and eventually
   in `setup.cfg` if you want to ship and install your package via `pip` later on.
2. Create concrete dependencies as `environment.lock.yml` for the exact reproduction of your
   environment with:
   ```bash
   conda env export -n {{cookiecutter.__pkg_import_name}} -f environment.lock.yml
   ```
   For multi-OS development, consider using `--no-builds` during the export.
3. Update your current environment with respect to a new `environment.lock.yml` using:
   ```bash
   conda env update -f environment.lock.yml --prune
   ```

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
│   └── {{cookiecutter.__pkg_import_name}}      <- Actual Python package where the main functionality goes.
├── tests                   <- Unit tests which can be run with `pytest` or `nox`.
├── .pre-commit-config.yaml <- Configuration of pre-commit git hooks.
├── CHANGELOG.md            <- Changelog to keep track of new features and fixes.
├── CONTRIBUTING.md         <- Documentation on how to contribute to the project.
├── dj_local_conf.json      <- DataJoint configuration file.
├── environment.yml         <- The conda environment file for reproducibility.
├── LICENSE                 <- Open source license.
├── mkdocs.yml              <- Configuration for building the documentation with MkDocs.
├── noxfile.py              <- `nox` automation file for continuous integration steps.
├── pyproject.toml          <- Build system configuration for the project.
|                              Only edit if absolutely necessary.
└── README.md               <- The top-level README for the repository.
```

<!--rest-of-doc-end-->
