# replay.sh

The same outcome as `cookiecutter --replay`, but using the generated `.cookiecutter.json` file instead of whatever was entered last.

**The `replay.sh --help` documentation**:

```
usage: replay.sh [OPTION]... [output_directory] cookiecutter_json

Regenerate cookiecutter content

Options:

-h, --help, help ... Show this help then exit.

-r .... Repository url.
        Value=wf

-d .... Template subdirectory to use from multi-template repository url.
        Value=flit

-n .... Conda environment name that contains cookiecutter.
        Value=cookies

-f .... Force remove existing content on rebuild.
        Value=false


Positional args:

output_directory .... The directory where the output will be generated.
                      Value=dj-cookiecutter/flit/replay/build/

cookiecutter_json ... Path to the '.cookiecutter.json' file with user config. (Required)
                      Value=


Examples:

 Regenerate to directory 'build' using previously specified values.
   > ./replay.sh path/to/.cookiecutter.json

 Regenerate to current directory using a different repo and branch, also conda env.
   > ./replay.sh -d flit -r https://github.com/iamamutt/dj-cookiecutter.git -n cookies . path/to/.cookiecutter.json

 Use local cloned content to rebuild
   > ./replay.sh -r path/to/template path/to/.cookiecutter.json
```

## Requirements

- `conda` environment with required packages installed
  - `cookiecutter` python package
- `bash`
- a `.cookiecutter.json` file with the user specified values filled in. See this [`.cookiecutter.json`](../{{cookiecutter.github_repo}}/.cookiecutter.json) as an example.

## Example Usage

1. Install `cookiecutter` as outlined [here](../README.md#install-cookiecutter).

2. Change to a temporary directory then clone the repo to get `replay.sh`.

   - `cd /tmp`
   - `git clone https://github.com/datajoint-company/dj-cookiecutter.git`

3. Use the template.

   - `cd /tmp/dj-cookiecutter`
   - `cookiecutter --directory flit .`

4. Run `replay.sh`.

   - `cd /tmp/wt-causality-in-motion`
   - `../dj-cookiecutter/flit/replay/replay.sh . .cookiecutter.json`
