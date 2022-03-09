# dj-cookiecutter
***Drew Yang @ DataJoint*** | ***2022.02.18***

---

This is a customized Cookiecutter python project template that you can generate an inital python project directory structure and common-used files

- Cookiecutter: [Cookiecutter Github](https://github.com/cookiecutter/cookiecutter/tree/1.7.2)
- Reference: [cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage), a python Cookiecutter template that managed by Cookiecutter team

---

## Generate a python project
**Prerequisite**
```
pip install cookiecutter
```

**Refer template from github repo or local directory**
```
cookiecutter git@github.com:datajoint-company/dj-cookiecutter.git --directory workflow
# set value to each variable, or skip to use default value
# a python project will be generated at ~/Project/project_name/


# or if there is an existing cookiecutter template: ./existing_cookiecutter
cookiecutter ./existing_cookiecutter --directory workflow

# generate a project to a specific directory: ./Projects
cookiecutter git@github.com:datajoint-company/dj-cookiecutter.git --directory workflow -o ./Project
# files will be in ./Projects/project_name

# this repo supports multiple cookiecutter templates
cookiecutter git@github.com:datajoint-company/dj-cookiecutter.git --directory element

# if you have already started working on your project and there are existing files
cookiecutter git@github.com:datajoint-company/dj-cookiecutter.git --directory workflow --overwrite-if-exists
# or
cookiecutter git@github.com:datajoint-company/dj-cookiecutter.git --directory workflow --skip-if-file-exists
```

> Note: cookiecutter will cache/clone this specified template repo to your user directory's ~/.cookiecutters

> Note: the [`flit`](flit/README.md) template requires _cookiecutter>=2.0.0_

**context of cookiecutter.json**
```
{
    "author_name":  # author name in setup.py and LICENSE
    "author_email": # author email in setup.py
    "project_name": # uncleaned project name, might contain space or dash
    "project_slug": # please skip, by default automatically replace space in 'project_name' by underscore
    "license": # license options that predefined under ~/dj-cookiecutter/{{cookiecutter.project_slug}}/LICENSE
}
```
## Roughly explain
`cookiecutter` cmd will find the `cookiecutter.json` file under the specified template directory whether it's on local or on github, and take each key-value pair as `{variable : default value}`. It will ask you to input a value for each variable to replace the default value. Then, it will use `Jinja` to embed each variable to each file name, folder name or file content that refered it.


If you want to know more details, read this [page](https://cookiecutter.readthedocs.io/en/1.7.2/first_steps.html), it explains the basic logic about how cookiecutter works.

## Existing template
- [flit](https://github.com/datajoint-company/dj-cookiecutter/tree/main/flit) by @iamamutt
- [cicd](#) by @Yambottle
- `workflow/element` created as initial examples for science-team, welcome changes or new templates for your own requirements


---
## License
© Datajoint, 2022. Licensed under an MIT license.
