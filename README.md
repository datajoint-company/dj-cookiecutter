# dj-cookiecutter

**_Drew Yang @ DataJoint_** | **_2022.02.18_**

**_Joseph Burling @ DataJoint_** | **_2022.04.08_**

---

This is a customized Cookiecutter python project template that you can generate an inital python project directory structure and common-used files

- [**Cookiecutter Github**](https://github.com/cookiecutter/cookiecutter)
- [**Cookiecutter Docs**](https://cookiecutter.readthedocs.io/en/2.0.2/)

---

## Cookiecutter usage and installation

### Installation

```
pip install -U "git+https://github.com/cookiecutter/cookiecutter" tomli pyyaml
```

### Basic usage

Use the `cookiecutter` command-line interface to generate new projects. You need to reference the name of the template folder and point to a GitHub repo or a local directory that holds the template. You will be asked to set a value for each variable, or you can skip (press `ENTER`) to use the default values.

Example, use the template corresponding to the folder `template-name` and point to the GitHub repo containing the templates at `git@github.com:...` (you can also use `gh:` as a shorthand for `git@github.com:`).

> **Note**: Make sure the `cookiecutter` cli can be found, activating the environment if necessary!

```
cookiecutter --directory template-name git@github.com:datajoint-company/dj-cookiecutter.git
```

A python project will be generated at `~/.../my-current-dir/project-name/`, where `project-name` is determined based on your input to the questions asked.

If there is an existing, local cookiecutter template, e.g., at `./dj-cookiecutter`, you can use that path instead of the GitHub repo url.

```
cookiecutter --directory template-name ./dj-cookiecutter
```

### Specifying additional options

To generate a project to a specific directory: `./Projects`

```
cookiecutter --directory template-name -o ./Project gh:datajoint-company/dj-cookiecutter
```

Files will be in `./Projects/project_name`.

If you have already started working on your project and there are existing files.

```
cookiecutter --directory template-name --overwrite-if-exists gh:datajoint-company/dj-cookiecutter 
```

or ...

```
cookiecutter --directory template-name --skip-if-file-exists gh:datajoint-company/dj-cookiecutter
```

This repo uses multiple cookiecutter templates, requiring the `--directory` option. To specifiy a different template, e.g., `another-template`:

```
cookiecutter --directory another-template gh:datajoint-company/dj-cookiecutter 
```

> **Note**: cookiecutter will cache/clone this specified template repo to your user directory's ~/.cookiecutters

--- 

## DataJoint Templates

- [`datajoint-workflow`](datajoint-workflow/README.md) by @Yambottle, @iamamutt
- [`element-example`](element-example/README.md) created as initial examples for science-team, welcome changes or new templates for your own requirements
- [`basic-package`](basic-package/README.md) by @iamamutt
- 
> Note: the [`datajoint-workflow`](datajoint-workflow/README.md) and [`basic-package`](basic-package/README.md) templates require _cookiecutter>=2.0.0_

--- 

## General `cookiecutter` Overview

The `cookiecutter` cmd will find the `cookiecutter.json` file under the specified template directory whether it's on local or on github, and take each key-value pair as `{variable : default value}`. It will ask you to input a value for each variable to replace the default value. Then, it will use `Jinja` to embed each variable to each file name, folder name or file content that refered it.

_Example context of cookiecutter.json._

```
{
    "author_name":  # author name in setup.py and LICENSE
    "author_email": # author email in setup.py
    "project_name": # uncleaned project name, might contain space or dash
    "project_slug": # please skip, by default automatically replace space in 'project_name' by underscore
    "license": # license options that predefined under ~/dj-cookiecutter/{{cookiecutter.project_slug}}/LICENSE
}
```

If you want to know more details, read this [page](https://cookiecutter.readthedocs.io/en/2.0.2/tutorial1.html), it explains the basic logic about how cookiecutter works.

---

## License

© Datajoint, 2022. Licensed under an MIT license.
