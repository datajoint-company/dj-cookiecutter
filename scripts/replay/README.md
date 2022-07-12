# replay.sh

The same outcome as `cookiecutter --replay`, but using the generated `.cookiecutter.json` file instead of whatever was entered last.

**The `replay.sh --help` documentation**:

```
usage: replay.sh [OPTION]... output_directory [cookiecutter_json]

Regenerate cookiecutter content

Options:

-h, --help, help ... Show this help then exit.

-r .... Repository url.
        Value=https://github.com/datajoint-company/dj-cookiecutter.git

-d .... Template subdirectory to use from multi-template repository url.
        Value=datajoint-workflow

-n .... Conda environment name that contains cookiecutter.
        Value=cookies


Positional args:

output_directory .... The directory where the output will be generated. (Required)
                      Value=

cookiecutter_json ... Path to the '.cookiecutter.json' file with user config.
                      Value=/.cookiecutter.json


Examples:

 Regenerate to directory 'build' using previously specified values.
   > ./replay.sh path/to/project

 Regenerate to current directory using a different repo and branch, also conda env.
   > ./replay.sh -d datajoint-workflow -r https://github.com/iamamutt/dj-cookiecutter.git -n cookies path/to/project diff/.cookiecutter.json

 Use local cloned content to rebuild
   > ./replay.sh -r path/to/project
```

## Requirements

- `conda` environment with required packages installed
  - `tomli`, 
  - `pyyaml`
  - [`cookiecutter` ](https://github.com/cookiecutter/cookiecutter)
  - [`retrocookie`](https://github.com/iamamutt/retrocookie)
- `bash`
- a `.cookiecutter.json` file with the user specified values filled in. This will be automatically generated at the root of the project folder.

## Example Usage

1. Install `cookiecutter` as outlined [here](../README.md#install-cookiecutter).

2. Change to a temporary directory then clone the repo to get `replay.sh`.

   - `cd /tmp`
   - `git clone https://github.com/datajoint-company/dj-cookiecutter.git`

3. Use the template.

   - `cd /tmp/dj-cookiecutter`
   - `cookiecutter --directory datajoint-workflow .`

4. Run `replay.sh`.

   - `cd /tmp/science-institute_brain-lab`
   - `../dj-cookiecutter/datajoint-workflow/scripts/replay/replay.sh . .cookiecutter.json`
