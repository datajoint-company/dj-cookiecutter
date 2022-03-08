#!/bin/bash --login

# scripts/cookiecutter/make.sh --help
# scripts/cookiecutter/make.sh -r https://github.com/iamamutt/dj-cookiecutter.git

script_cmd="${BASH_SOURCE[0]}"
script_pdir="$(cd "$(dirname "${script_cmd}")" &>/dev/null && pwd)"
script_file=$(basename "${script_cmd}")

template_dir=flit
repo_url=wf
conda_env=cookies
build_dir="${script_pdir}/build/"
delete_existing=false

SHOW_HELP=0
show_help() {
	echo "usage: $script_file [OPTION]... build_dir

Regenerate cookiecutter content

Options:

-h, --help, help ... Show this help then exit.

-r .... Repository url.
          Default=https://github.com/datajoint-company/dj-cookiecutter.git
-d .... Template directory to use from multi-template repository url.
          Default='flit'
-n .... Conda environment name.
          Default='cookies'
-f .... Force remove existing content on rebuild.
          Default=false

Examples:

 Regenerate to directory 'build' using previously specified values.
   > $script_file build

 Regenerate to current directory using a different repo and branch, also conda env.
   > $script_file -d flit -r https://github.com/iamamutt/dj-cookiecutter.git -n cookies .

 Use local cloned content to build
   > $script_file -r path/to/template ./build
"
	exit 0
}

while [[ $# -gt 0 ]]; do
	case "$1" in
	"help" | "--help" | "-h")
		SHOW_HELP=1
		break
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
		shift
		;;
	*)
		build_dir="${1}"
		shift
		;;
	esac
done

# show help if asked
# ------------------

[[ ${SHOW_HELP} -eq 1 ]] && show_help

conda activate "${conda_env}"

if [[ -d "${build_dir}" ]]; then
	echo "Directory 'build' already exists. Overwriting existing content."
	[[ ${delete_existing} = true ]] && rm -rf "${build_dir}"
fi

echo "command: cookiecutter --overwrite-if-exists --no-input --config-file "${script_pdir}/cookiecutterc.yml" --debug-file "${script_pdir}/cookiecutter.log" --output-dir "${build_dir}" --directory "${template_dir}" "${repo_url}""

cookiecutter \
	--overwrite-if-exists --no-input \
	--config-file "${script_pdir}/cookiecutterc.yml" \
	--debug-file "${script_pdir}/cookiecutter.log" \
	--output-dir "${build_dir}" \
	--directory "${template_dir}" \
	"${repo_url}"
