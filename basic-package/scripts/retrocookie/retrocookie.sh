#!/bin/bash --login

# datajoint-workflow/scripts/retrocookie/retrocookie.sh --help

script_cmd="${BASH_SOURCE[0]}"
script_pdir="$(cd "$(dirname "${script_cmd}")" &>/dev/null && pwd)"
script_file=$(basename "${script_cmd}")
curr_dir=$PWD

root_dir=$(cd "${script_pdir}"/../../.. &>/dev/null && pwd)
template_dir="datajoint-workflow"
conda_env=cookies
cc_config=
pos_args=()
ignores=()

err_exit() {
	set -e
	echo "#! Error: $*" >&2
	return 1
}

SHOW_HELP=0
show_help() {
	echo "usage: $script_file [OPTION]... project_folder cc_config

Convert modified cookiecutter output back to it's template form.

Options:

-h, --help, help ... Show this help then exit.

-d .... Template subdirectory to use from multi-template repository url.
        Value=$template_dir

-n .... Conda environment name that contains cookiecutter.
        Value=$conda_env

-i .... Ignore a file/folder from commits by adding it to .gitignore


Positional args:

project_folder .... The directory corresponding to the output of the original
                    cookiecutter command.
                    Value=$project_folder
cc_config ......... Path to the 'cookiecutterc.yml' file with preconfigured values.
                    Value=$cc_config

Temporary copy directory:

$tmp_proj_parent

Examples:

 Regenerate to directory 'build' using previously specified values.
   > ./$script_file path/to/workflow_name

 Regenerate to current directory using a different repo and branch, also conda env.
   > ./$script_file -d datajoint-workflow -n cookies path/to/workflow_name

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
	"-n")
		conda_env="${2}"
		shift
		shift
		;;
	"-i")
		ignores+=("${2}")
		shift
		shift
		;;
	*)
		pos_args+=("${1}")
		shift
		;;
	esac
done


if [[ ${#pos_args[@]} -lt 2 ]]; then
	project_folder=${pos_args[0]:-my_project_dir}
	cc_config="${project_folder}/.cookiecutter.json"
else
	project_folder=${pos_args[0]}
	cc_config=${pos_args[1]}
fi

tmp_proj_parent=${TMPDIR:-~/tmp/}cookie_retro/${template_dir}

# show help if asked
# ------------------
[[ ${SHOW_HELP} -eq 1 ]] && show_help

{ [[ -z "$project_folder" ]] || [[ ! -d "$project_folder" ]]; } && err_exit "project folder path is required."
project_folder=$(cd "${project_folder}" &>/dev/null && pwd)
rm -rf "${tmp_proj_parent}"
mkdir -p "${tmp_proj_parent}"

conda activate "${conda_env}"

if [[ -f ${cc_config} ]]; then
	python "${script_pdir}"/../replay2config.py "${cc_config}" "${tmp_proj_parent}/cookiecutterc.yml"
	cc_config="${tmp_proj_parent}/cookiecutterc.yml"
else
	cc_config="${root_dir}/tests/integration/fixtures/cookiecutterc.yml"
fi

echo -e "\n============ Project configuration context ============"
echo -e "\n> '$cc_config'"

echo -e "\n============ Generating default content from template."
echo -e "\n> command: 'cookiecutter --overwrite-if-exists --no-input --output-dir=${tmp_proj_parent}  --config-file=${cc_config} --directory=${template_dir} ${root_dir}'"

cookiecutter --overwrite-if-exists --no-input \
	--output-dir="${tmp_proj_parent}" \
	--config-file="${cc_config}" \
	--directory="${template_dir}" \
	"${root_dir}"

tmp_proj_dir="$(cd "$(dirname "${tmp_proj_parent}"/*/.cookiecutter.json)" &>/dev/null && pwd)"
[[ ! -f ${tmp_proj_dir}/.cookiecutter.json ]] && err_exit ".cookiecutter.json must exist"

rev_num=0
COMMIT=HEAD

create_commits() {
	echo -e "\n============ Checking if needing to commit new files ============"
	cd "${tmp_proj_dir}"
	# git config --global init.defaultBranch main
	git init >/dev/null
	git add .
	git commit -m "initial commit" --no-verify >/dev/null
	rm -rf "${tmp_proj_parent}"/.git
	mv -f "${tmp_proj_dir}"/.git "${tmp_proj_parent}"
	rm -rf "${tmp_proj_dir:?}"
	mkdir -p "${tmp_proj_dir}"
	rsync -av --quiet "${project_folder}" "${tmp_proj_dir}"/.. --exclude .git --exclude .ipynb_checkpoints --exclude .nox --exclude .mypy_cache --exclude .pytest_cache
	mv -f "${tmp_proj_parent}/.git" "${tmp_proj_dir}"/
	cd "${tmp_proj_dir}"
	if [[ ${#ignores} -gt 0 ]]; then
		echo -e "\n----------- Adding paths to .gitignore."
		echo -e "\n# Added by retrocookie script ignore option" >>.gitignore
		for _ex in "${ignores[@]}"; do
			echo "Removing: '${_ex}'"
			echo "${_ex}" >>.gitignore
		done
		git add .gitignore
		git commit -m "Added by retrocookie script ignore option" --no-verify
	fi
	if [[ ! $(git status --porcelain) ]]; then
		echo -e "\nnothing to change"
		cd "${curr_dir}"
		exit 0
	fi
	echo -e "\n----------- Adding and committing new files."
	git add . :^src/*/version.py
	git commit -m "build(retrocookie): reflect updates to source template from generated project '$(basename "${tmp_proj_dir}")'" --no-verify
	COMMIT=$(git rev-parse HEAD)
	rev_num=$((rev_num + 1))

	# local untracked=false
	# local modified=false
	# local deleted=false
	# [[ $(git status --porcelain | grep "^??") ]] && untracked=true
	# [[ $(git status --porcelain | grep "^ M") ]] && modified=true
	# [[ $(git status --porcelain | grep "^ D") ]] && deleted=true
	#
	# [[ $untracked = false ]] && echo "delete" >"._junk"
	# [[ $modified = true ]] && git stash
	# git add .
	# git commit -m "build(retrocookie): add to template from altered project"
	# rev_num=$((rev_num + 1))
	# [[ $modified = true ]] && git stash pop
	#
	# echo -e "\n----------- Checking if needing to commit modified files"
	# if [[ $modified = true ]]; then
	# 	git add -u
	# 	git commit -m "build(retrocookie): update modified template from altered project"
	# 	rev_num=$((rev_num + 1))
	# fi

	echo -e "\n----------- Commits completed"
	echo "Remember to git cherry-pick --continue if required."
	echo "Found $rev_num commits"
	git rev-list main
	cd "${curr_dir}"
}

create_commits

(
	cd "${root_dir}"
	# code "${root_dir}"
	echo -e "\n============ Cherry-picking commits ============"
	if [[ $rev_num -gt 1 ]]; then
		echo "command: retrocookie --directory='$template_dir' --exclude-variable=_pkg_version '$tmp_proj_dir' HEAD~$((rev_num - 1))"
		retrocookie --directory="${template_dir}" --exclude-variable=_pkg_version "${tmp_proj_dir}" HEAD~$((rev_num - 1))
	else
		echo "command: retrocookie --directory='$template_dir' --exclude-variable=_new_lines --exclude-variable=_pkg_version '$tmp_proj_dir' HEAD"
		if [[ $(retrocookie --directory="${template_dir}" --exclude-variable=_new_lines --exclude-variable=_pkg_version "${tmp_proj_dir}" $COMMIT) ]]; then
			echo -e "\nFound merge conflicts."
		else
			git reset --soft HEAD^1
		fi
	fi
)
