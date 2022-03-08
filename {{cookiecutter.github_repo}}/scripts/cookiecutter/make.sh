#!/bin/bash --login

# ./make.sh flit https://github.com/iamamutt/dj-cookiecutter.git cookies

script_pdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

git_branch="${1:-flit}"
repo_url="${2:-wf}"
conda activate "${3:-cookies}"

if [[ -d "${script_pdir/build/}" ]]; then
	echo "Directory 'build' already exists. Replacing existing content."
	rm -rf "${script_pdir/build/}"
fi

(
	cd "${script_pdir}" || exit 1
	cookiecutter \
		--config-file cookiecutterc.yml \
		--debug-file cookiecutter.log \
		--overwrite-if-exists --no-input --output-dir build \
		--checkout "${git_branch}"
	${repo_url}
)
