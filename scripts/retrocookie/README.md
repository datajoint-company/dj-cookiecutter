# retrocookie.sh

You can add changes back to a template folder using the [`retrocookie`](https://retrocookie.readthedocs.io/en/latest/) python package. [This fork](https://github.com/iamamutt/retrocookie) fixes use of multiple template folders.

**The `retrocookie.sh --help` documentation**:

```
usage: retrocookie.sh [OPTION]... project_folder cc_config

Convert modified cookiecutter output back to it's template form.

Options:

-h, --help, help ... Show this help then exit.

-d .... Template subdirectory to use from multi-template repository url.
        Value=datajoint-workflow

-n .... Conda environment name that contains cookiecutter.
        Value=cookies

-i .... Ignore a file/folder from commits by adding it to .gitignore


Positional args:

project_folder .... The directory corresponding to the output of the original
                    cookiecutter command.
                    Value=my_project_dir
cc_config ......... Path to the 'cookiecutterc.yml' file with preconfigured values.
                    Value=my_project_dir/.cookiecutter.json

Temporary copy directory:

/var/folders/t3/wwync7qs1753cd1nzlqnzt900000gn/T/cookie_retro/datajoint-workflow

Examples:

 Regenerate to directory 'build' using previously specified values.
   > ./retrocookie.sh path/to/workflow_name

 Regenerate to current directory using a different repo and branch, also conda env.
   > ./retrocookie.sh -d datajoint-workflow -n cookies path/to/workflow_name
```

## Requirements

- `conda` environment with required packages installed
  - `tomli`, 
  - `pyyaml`
  - [`cookiecutter` ](https://github.com/cookiecutter/cookiecutter)
  - [`retrocookie`](https://github.com/iamamutt/retrocookie)
- `bash` with `rsync` and `git` found in `PATH`.
- A project generated from a cookiecutter template.
- a `.cookiecutter.json` file with the user specified values filled in. This will be automatically generated at the root of the project folder.

## Example Usage

1. Install `cookiecutter` as outlined [here](../../README.md#install-cookiecutter).

2. Install `retrocookie`: `pip install 'git+https://github.com/iamamutt/retrocookie'`

3. Clone the repo contents.

   - `git clone https://github.com/datajoint-company/dj-cookiecutter.git`
   - _Optional_: Edit `dj-cookiecutter/tests/integration/fixtures/cookiecutterc.yml`. The rest of the instructions below assume these default values.

4. Use the template.

   - `cookiecutter -f --no-input --config-file=dj-cookiecutter/tests/integration/fixtures/cookiecutterc.yml --directory=datajoint-workflow -o /tmp dj-cookiecutter`

5. Make some changes to files in `/tmp/science-institute_brain-lab`.

6. Run `retrocookie.sh`

   - `dj-cookiecutter/datajoint-workflow/scripts/retrocookie/retrocookie.sh /tmp/science-institute_brain-lab`

_Note:_ If you run into merge conflicts, see the help for [`git-cherry-pick`](https://git-scm.com/docs/git-cherry-pick).
