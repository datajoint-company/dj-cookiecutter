import json
import sys

import yaml


def replay2config(args):
    if not args:
        raise FileNotFoundError(
            "Need location of replay file and config file as input arguments."
        )

    replay_file, config_file = args[:2]

    with open(replay_file, "r") as fin:
        jsf = json.load(fin)

    entries = {
        "abbreviations": {
            "djcc": "https://github.com/datajoint-company/dj-cookiecutter.git"
        },
        "default_context": {
            k: v for k, v in jsf.items() if not k.startswith("_copy_without_render")
        },
    }

    with open(config_file, "w") as fout:
        yaml.safe_dump(entries, fout)


if __name__ == "__main__":
    replay2config(sys.argv[1:])
