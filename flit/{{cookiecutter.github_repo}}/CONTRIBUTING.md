<!--start-contrib-->

# Contributing

Welcome to the `{{cookiecutter.__project_name}}` contributor's guide.

This document focuses on getting any potential contributor familiarized with the development process, but [other kinds of contributions](https://opensource.guide/how-to-contribute) are also appreciated. See the DataJoint [community contributions](https://docs.datajoint.org/python/community/02-Contribute.html) page for information.

If you are new to using [git](https://git-scm.com) or have never collaborated in a project previously, please have a look at [contribution-guide.org](http://www.contribution-guide.org/). Other resources are also listed in the excellent [guide created by FreeCodeCamp](https://github.com/FreeCodeCamp/how-to-contribute-to-open-source).

!!! note "Python Code of Conduct"
    Please notice, all users and contributors are expected to be **open, considerate, reasonable, and respectful**. When in doubt, [Python Software Foundation's Code of Conduct](https://www.python.org/psf/conduct/) is a good reference in terms of behavior guidelines.

## Issue Reports

If you experience bugs or general issues with `{{cookiecutter.__project_name}}`, please have a look at the [issue tracker]({{cookiecutter.__github_url}}/issues). If you don't see anything useful there, please feel free to fill out a new issue report.

New issue reports should include information about your programming environment (e.g., operating system, Python version) and steps to reproduce the problem. Please also try to simplify the reproduction steps to a very minimal example that still illustrates the problem you're facing. By removing other factors, you help us to identify the root cause of the issue.

!!! tip "Closed Issues"
    Please don't forget to include the closed issues in your search.
    Sometimes a solution was already reported, and the problem is considered **solved**.

## Documentation Improvements

You can help improve the `{{cookiecutter.__project_name}}` docs by making them more readable and coherent, or by adding missing information and correcting mistakes.

!!! tip "Quick Documentation Changes"
    Please notice that the [GitHub web interface](https://docs.github.com/en/github/managing-files-in-a-repository/managing-files-on-github/editing-files-in-your-repository) provides a quick way of propose changes in `{{cookiecutter.__project_name}}`'s files. While this mechanism can be tricky for normal code contributions, it works perfectly fine for contributing to the docs, and can be quite handy.

`{{cookiecutter.__project_name}}` documentation uses [MkDocs](https://www.mkdocs.org/) as its main documentation compiler. This means that the docs are kept in the same repository as the project code, and that any documentation update is done in the same way as a code contribution.

All documentation is written in [Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax), specifically the [`python-markdown`](https://python-markdown.github.io/#differences) implementation with additional [extensions](https://docutils.sourceforge.io/docs/ref/rst/directives.html#specific-admonitions) to use features from reStructuredText.

!!! tip "Google Style Docstrings"
    Most documentation is attached directly to python objects and
    written in the Google style to faciliate markdown parsing. See
    [Google style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) for examples.

When working on documentation changes in your local machine, you can compile them using `mkdocs serve`, and use Python's built-in web server for a preview in your web browser (`http://localhost:8000`). See the [Extra docs packages](#extra-docs-packages) section below for more details.

## Code Contributions

There are several ways to contribute code to the project, but first, create a user account on GitHub if you do not already have one. Any contributor changes should be reported as an issue, or proposed as a pull request (PR) from their **own fork**.

### Submit an Issue

Before you work on any non-trivial code contribution, it's best to first create a report in the [issue tracker]({{cookiecutter.__github_url}}/issues) to start a discussion on the subject. This often provides additional considerations and avoids unnecessary work.

### Submit Your Contribution

You can contribute code by cloning the repository content from your fork, then creating a new branch, [setting up a local development environment](#setting-up-a-local-development-environment), making changes, then submitting a [pull request]({{cookiecutter.__github_url}}/pull) to review and accept those changes.

#### Implement your changes on a new branch

After cloning, create a branch to hold your changes then start making edits. Try to avoid working on the master/main branch if possible to avoid triggering automated build steps later on. use [`git`](https://git-scm.com) to create a new branch.

```bash
git checkout -b my-feat-branch
```

Start your work on `my-feat-branch` branch. Don't forget to add [docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) to new functions, modules and classes, especially if they are part of public APIs.

When you're done editing, and to record your changes in `git`, do:

```bash
git add <MODIFIED FILES>
git commit
```

Format your commit messages so that they help create the appropriate semantic version number using conventional commit messages.

_Conventional Commit Resources_:

- [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/)
- [More commit examples](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional)
- [Angular format](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commit-message-format)

!!! tip "Commit History"
    Writing a [descriptive commit message](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commit-message-format) is highly recommended. In case of doubt, you can check the commit history to look for recurring communication patterns with:

        git log --graph --decorate --pretty=oneline --abbrev-commit --all

#### Submitting a pull request

If everything works fine, push your local branch to your GitHub repository fork with:

```
git push -u origin my-feat-branch
```

Go to the web page of your fork and click "Create pull request" to send your changes for review. Find more detailed information in [creating a PR](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request). You might also want to open the PR as a draft first and mark it as ready for review _after_ getting feedback from the continuous integration (CI) system, or any required fixes.

## Setting up a Local Development Environment

See the [_Installation_](./README.md#installation) section from the introductory documentation to first setup a local python virtual environment.

Install the extra packages needed for local development, tests, and documentation:

```bash
cd "{{cookiecutter.__project_name}}"
conda activate {{cookiecutter.__pkg_import_name}}
flit install --symlink --deps=develop
```

### Extra dev packages

The list of `dev` packages are specified in `pyproject.toml` under `[project.optional-dependencies.dev]`

#### `nox`

The [`nox`](https://nox.thea.codes/en/stable/tutorial.html) python package is used to automate a lot of the tasks, such as testing or building the documentation. For a list of command-line options, see:

```bash
nox --help
```

You can also use `nox` to run several other pre-configured tasks for this project. Try `nox -l` to see a list of the available tasks/sessions.

#### `pre-commit`

The [`pre-commit`](https://pre-commit.com/) package is used to detect or fix common issues before code is submitted to the remote repository. You first have to set and install the hooks after cloning the repository from GitHub. The `{{cookiecutter.__project_name}}` package comes with a lot of hooks configured to automatically help you check the code after being written. View the configuration in the file `.pre-commit-config.yaml`. Installing `pre-commit` and the specificed hooks is required only once:

```bash
pre-commit install --install-hooks
```

You might also want to run `pre-commit autoupdate` to get the latest version of the hooks. You can also do a first pass of `pre-commit` to fix anything that needs fixing so that any future commits only process the necessary files:

```bash
pre-commit run --all-files
```

!!! tip
    The `-n, --no-verify` flag of `git commit` can be used to deactivate pre-commit hooks temporarily.

### Extra test packages

The list of `test` packages are specified in `pyproject.toml` under `[project.optional-dependencies.test]`

#### `pytest`

The [`pytest`](https://docs.pytest.org/) package is used to run integration and unit tests in the `./tests` subdirectory.

You can run `pytest` directly, see the help:

```bash
pytest --help
```

or use `nox` to run the pre-specified tests in the `noxfile.py` file.

```bash
nox -s pytest
```

!!! important
    Don't forget to add unit tests and documentation in case your contribution adds an additional feature and is not just a bugfix. Then please check that your changes don't break any unit tests with:

        nox -s pytest

### Extra docs packages

The list of `docs` packages are specified in `pyproject.toml` under `[project.optional-dependencies.doc]`

The first time you clone your repo, run the following command to set the default docs alias to `latest` and create the `gh-pages` branch on remote. This also creates an `index.html` file at the root of the pages branch.

```bash
mike set-default --push latest
```

Use `nox` to build and deploy the latest docs (swap out `v0.0` for the latest version number):

```bash
nox -s docs -- --version v0.0
```

You can also build and deploy the latest docs with the following command:

```bash
mike deploy --push --update-aliases v0.0 latest
mike serve
```

See help for more information:

```bash
mike deploy --help
```

!!! note "GitHub Pages Settings"
    If your [pages url](${{cookiecutter.__url_documentation}}) is not loading, make sure you set the **Source** in your [pages settings](${{cookiecutter.__github_url}}/settings/pages) to `gh-pages` and use the _root_ directory. Pages will then be built and deployed with the pages url as the default.

_Documentation Resources_:

- builder: [`mkdocs`](https://www.mkdocs.org/user-guide)
- builder: [`mike`](https://github.com/jimporter/mike)
- theme: [`mkdocs-material`](https://squidfunk.github.io/mkdocs-material/setup/)
- markdown extensions: [`python-markdown`](https://python-markdown.github.io/extensions/md_in_html/)
- plugin: [`mkdocstrings`](https://mkdocstrings.github.io/usage/)

### Environment maintenance 

Exporting python packages:

```
mamba env export -n {{cookiecutter.__pkg_import_name}} -f environment.lock.yml --no-builds
```

Resetting environment to locked state:

```
mamba env update -f environment.lock.yml --prune
```

### GitHub Actions

The GitHub actions and workflows are located under the `.github` folder and automate many of the tasks previously outlined. The following actions are used:

- Checking out repo content: [actions/checkout@v3](https://github.com/actions/checkout)
- Caching python envs: [actions/cache@v2](https://github.com/actions/cache)
- Version tagging from commits: [mathieudutour/github-tag-action@v6.0](https://github.com/mathieudutour/github-tag-action)
- Create a release: [ncipollo/release-action@v1](https://github.com/ncipollo/release-action)
- Using `nox`: [excitedleigh/setup-nox@v2](https://github.com/excitedleigh/setup-nox)

### Troubleshooting

The following tips can be used when facing problems to build or test the
package:

Make sure to fetch all the tags from the upstream [repository]({{cookiecutter.__github_url}}). The command `git describe --abbrev=0 --tags` should return the version you are expecting. If you are trying to run CI scripts in a forked repository, make sure to push all the tags. You can also try to remove all the egg files or the complete egg folder, i.e., `.eggs`, as well as the `*.egg-info` folders in the `src` folder or potentially in the root of your project.

[Pytest can drop you](https://docs.pytest.org/en/stable/usage.html#dropping-to-pdb-python-debugger-at-the-start-of-a-test) in an interactive session in the case an error occurs. In order to do that you need to pass a `--pdb` option (for example by running `pytest <NAME OF THE FALLING TEST> --pdb`). You can also setup breakpoints manually instead of using the `--pdb` option.

<!--end-contrib-->
