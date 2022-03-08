#!/bin/bash --login

script_cmd="${BASH_SOURCE[0]}"
script_pdir="$(cd "$(dirname "${script_cmd}")" &>/dev/null && pwd)"
script_file=$(basename "${script_cmd}")

git_branch=flit
repo_url=wf
conda_env=cookies
build_dir="${script_pdir/build/}"
delete_existing=false

SHOW_HELP=0
show_help() {
	echo "usage: $script_file [OPTION]... build_dir

Regenerate cookiecutter content

Options:

-h, --help, help ... Show this help then exit.

-r .... Repository url.
          Default=https://github.com/datajoint-company/dj-cookiecutter.git
-b .... Branch to checkout from repository url. Set to '-' for no branch selection.
          Default='flit'
-n .... Conda environment name.
          Default='cookies'
-d .... Delete existing content on rebuild.
          Default=false

Examples:

 Regenerate to directory 'build' using previously specified values.
   > $script_file build

 Regenerate to current directory using a different repo and branch, also conda env.
   > $script_file -b flit -r https://github.com/iamamutt/dj-cookiecutter.git -n cookies .

 Use local cloned content to build
   > $script_file -b - -r  path/to/template ./build
"
	exit 0
}

while [[ $# -gt 0 ]]; do
	case "$1" in
	"help" | "--help" | "-h")
		SHOW_HELP=1
		break
		;;
	"-b")
		git_branch="${2}"
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
	"-d")
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

[[ ${git_branch} = "-" ]] && git_checkout="" || git_checkout="--checkout ${git_branch}"

cookiecutter \
	--config-file "${script_pdir/cookiecutterc.yml/}" \
	--debug-file "${script_pdir/cookiecutter.log/}" \
	--overwrite-if-exists --no-input --output-dir "${build_dir}" \
	"${git_checkout}" "${repo_url}"
