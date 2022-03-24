# retrocookie.sh

You can add changes back to a template folder using the [`retrocookie`](https://retrocookie.readthedocs.io/en/latest/) python package. [This fork](https://github.com/iamamutt/retrocookie) enables use of multiple template folders.

**The `retrocookie.sh --help` documentation**:

```
usage: retrocookie.sh [OPTION]... project_folder

Convert modified cookiecutter output back to it's template form.

Options:

-h, --help, help ... Show this help then exit.

-c .... Path to the 'cookiecutterc.yml' file with preconfigured values.
        Value=dj-cookiecutter/flit/cookiecutterc.yml

-d .... Template subdirectory to use from multi-template repository url.
        Value=flit

-n .... Conda environment name that contains cookiecutter.
        Value=cookies

-i .... Ignore a file/folder from commits by adding it to .gitignore

Positional args:

project_folder .... The directory corresponding to the output of the original
                    cookiecutter command.
                    Value=


Examples:

 Regenerate to directory 'build' using previously specified values.
   > ./retrocookie.sh path/to/workflow_name

 Regenerate to current directory using a different repo and branch, also conda env.
   > ./retrocookie.sh -d flit -n cookies path/to/workflow_name
```

## Requirements

- `conda` environment with required packages installed
  - `cookiecutter` python package
  - `retrocookie` python package
- `bash` with `rsync` and `git` found in `PATH`.
- a `.cookiecutter.json` file at the root of the project with the user specified values. See this [`.cookiecutter.json`](../{{cookiecutter.github_repo}}/.cookiecutter.json) as an example.
- A project generated from a cookiecutter template.

## Example Usage

1. Install `cookiecutter` as outlined [here](../README.md#install-cookiecutter).

2. Install `retrocookie`: `pip install 'git+https://github.com/iamamutt/retrocookie'`

3. Clone the repo contents.

   - `git clone https://github.com/datajoint-company/dj-cookiecutter.git`
   - Edit `dj-cookiecutter/flit/cookiecutterc.yml`. The rest of the instructions below assume the default values.

4. Use the template.

   - `cookiecutter -f --no-input --config-file=dj-cookiecutter/flit/cookiecutterc.yml --directory=flit -o /tmp dj-cookiecutter`

5. Make some changes to files in `/tmp/wt-causality-in-motion`.

6. Run `retrocookie.sh`

   - `dj-cookiecutter/flit/retrocookie/retrocookie.sh /tmp/wt-causality-in-motion`

_Note:_ If you run into merge conflicts, see the help for [`git-cherry-pick`](https://git-scm.com/docs/git-cherry-pick).
