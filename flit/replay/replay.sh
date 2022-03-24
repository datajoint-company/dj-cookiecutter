#!/bin/bash --login

# flit/replay/replay.sh --help

script_cmd="${BASH_SOURCE[0]}"
script_pdir="$(cd "$(dirname "${script_cmd}")" &>/dev/null && pwd)"
script_file=$(basename "${script_cmd}")

template_dir=flit
repo_url=wf
conda_env=cookies
delete_existing=false
pos_args=()

err_exit() {
	set -e
	echo "#! Error: $*" >&2
	return 1
}

SHOW_HELP=0
show_help() {
	echo "usage: $script_file [OPTION]... [output_directory] cookiecutter_json

Regenerate cookiecutter content

Options:

-h, --help, help ... Show this help then exit.

-r .... Repository url.
        Value=$repo_url

-d .... Template subdirectory to use from multi-template repository url.
        Value=$template_dir

-n .... Conda environment name that contains cookiecutter.
        Value=$conda_env

-f .... Force remove existing content on rebuild.
        Value=$delete_existing


Positional args:

output_directory .... The directory where the output will be generated.
                      Value=$output_dir

cookiecutter_json ... Path to the '.cookiecutter.json' file with user config. (Required)
                      Value=$input_json


Examples:

 Regenerate to directory 'build' using previously specified values.
   > ./$script_file path/to/.cookiecutter.json

 Regenerate to current directory using a different repo and branch, also conda env.
   > ./$script_file -d flit -r https://github.com/iamamutt/dj-cookiecutter.git -n cookies . path/to/.cookiecutter.json

 Use local cloned content to rebuild
   > ./$script_file -r path/to/template path/to/.cookiecutter.json
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
	"-f")
		delete_existing=true
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

if [[ ${#pos_args} -lt 2 ]]; then
	output_dir="${script_pdir}/build/"
	input_json=${pos_args[0]}
else
	output_dir=${pos_args[0]}
	input_json=${pos_args[1]}
fi

[[ ${SHOW_HELP} -eq 1 ]] && show_help

{ [[ -z "$input_json" ]] || [[ ! -f "$input_json" ]]; } && err_exit ".cookiecutter.json file is required."

conda activate "${conda_env}"

if [[ -d "${output_dir}" ]]; then
	echo "Directory 'build' already exists. Overwriting existing content."
	[[ ${delete_existing} = true ]] && rm -rf "${output_dir}"
fi

replay_file=${script_pdir}/${template_dir}.cookiecutter.json
cat <<-EOF >"${replay_file}"
	{
	"cookiecutter": $(cat "$input_json")
	}
EOF

echo "command: cookiecutter --overwrite-if-exists --replay-file='${replay_file}' --debug-file='${script_pdir}/cookiecutter.log' --output-dir='${output_dir}' --directory='${template_dir}' '${repo_url}'"

cookiecutter \
	--overwrite-if-exists \
	--replay-file="${replay_file}" \
	--debug-file="${script_pdir}/cookiecutter.log" \
	--output-dir="${output_dir}" \
	--directory="${template_dir}" \
	"${repo_url}"
