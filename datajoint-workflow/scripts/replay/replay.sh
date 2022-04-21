#!/bin/bash --login

# datajoint-workflow/scripts/replay/replay.sh --help

echo "$0 $*"
script_cmd="${BASH_SOURCE[0]}"
script_pdir="$(cd "$(dirname "${script_cmd}")" &>/dev/null && pwd)"
script_file=$(basename "${script_cmd}")

template_dir=datajoint-workflow
repo_url=https://github.com/datajoint-company/dj-cookiecutter.git
conda_env=cookies
pos_args=()

err_exit() {
	set -e
	echo "#! Error: $*" >&2
	return 1
}

SHOW_HELP=0
show_help() {
	echo "usage: $script_file [OPTION]... output_directory [cookiecutter_json]

Regenerate cookiecutter content

Options:

-h, --help, help ... Show this help then exit.

-r .... Repository url.
        Value=$repo_url

-d .... Template subdirectory to use from multi-template repository url.
        Value=$template_dir

-n .... Conda environment name that contains cookiecutter.
        Value=$conda_env


Positional args:

output_directory .... The directory where the output will be generated. (Required)
                      Value=$output_dir

cookiecutter_json ... Path to the '.cookiecutter.json' file with user config.
                      Value=$input_json


Examples:

 Regenerate to directory 'build' using previously specified values.
   > ./$script_file path/to/project

 Regenerate to current directory using a different repo and branch, also conda env.
   > ./$script_file -d datajoint-workflow -r https://github.com/iamamutt/dj-cookiecutter.git -n cookies path/to/project diff/.cookiecutter.json

 Use local cloned content to rebuild
   > ./$script_file -r path/to/project
"
	exit 0
}

while [[ $# -gt 0 ]]; do
	case "$1" in
	"help" | "--help" | "-h")
		SHOW_HELP=1
		shift
		;;
	"-d")
		template_dir="${2}"
		shift
		shift
		;;
	"-r")
		repo_url="${2}"
		shift
		shift
		;;
	"-n")
		conda_env="${2}"
		shift
		shift
		;;
	*)
		pos_args+=("${1}")
		shift
		;;
	esac
done

# show help if asked
# ------------------

if [[ ${#pos_args[@]} -lt 2 ]]; then
	output_dir=${pos_args[0]}
	input_json="${output_dir}/.cookiecutter.json"
else
	output_dir=${pos_args[0]}
	input_json=${pos_args[1]}
fi

[[ ${SHOW_HELP} -eq 1 ]] && show_help

{ [[ -z "$input_json" ]] || [[ ! -f "$input_json" ]]; } && err_exit ".cookiecutter.json file not found at: '$input_json'"

conda activate "${conda_env}"

tmp_dir=${TMPDIR:-~/tmp/}cookie_replay/"${template_dir}"
rm -rf "${tmp_dir}"
mkdir -p "${tmp_dir}"
replay_file=${tmp_dir}/.cookiecutterc.yml
debug_file=${tmp_dir}/.cookiecutter.log
output_dir=$(dirname "$output_dir")

python "${script_pdir}"/../replay2config.py "${input_json}" "${replay_file}"

if [[ -d "${output_dir}" ]]; then
	echo "Directory '${output_dir}' already exists. Overwriting existing content."
fi

echo "command: cookiecutter --overwrite-if-exists --no-input --config-file='${replay_file}' --debug-file='${debug_file}' --output-dir='${output_dir}' --directory='${template_dir}' '${repo_url}'"

cookiecutter \
	--overwrite-if-exists \
	--no-input \
	--config-file="${replay_file}" \
	--debug-file="${debug_file}" \
	--output-dir="${output_dir}" \
	--directory="${template_dir}" \
	"${repo_url}"
