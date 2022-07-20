# syntax=docker/dockerfile:labs

# global arguments shared across different build stages
ARG TIMEZONE="America/Chicago"
ARG REPO_NAME=science-institute_brain-lab
ARG WORKFLOW_VERSION=v0.0.0
ARG IMAGE_CREATED=2022-11-11T11:11:11Z

## Stage 1 =============================================================================
## Core Debian Image w/ Conda (micromamba)
## -------------------------------------------------------------------------------------
FROM debian:11-slim as micromamba_debian

# inherit from global args
ARG TIMEZONE

# stage-specific args
ARG PY_VER=3.9
ARG MAMBA_INSTALL_ROOT=/opt/local/conda

# system environment
ENV TZ=${TIMEZONE}
ENV LANG=en_US.utf8
ENV LC_ALL=en_US.utf8
ENV LANGUAGE=en_US.utf8
ENV LC_CTYPE=en_US.utf8

# shell exit on first error within EOF sections
SHELL [ "/bin/sh", "-ec" ]

# script for common routine of installing and clearing debian packages
RUN cat <<-"EOF" >/usr/local/bin/apt-get-update-install
	#!/bin/bash
	[[ $# -lt 1 ]] && exit 0
	echo "# => Installing debian packages: '$*'"
	echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
	apt-get update >/dev/null
	apt-get -qq install -y --no-install-recommends "$@"
	apt-get autoremove -y
	apt-get clean -y
	rm -rf /var/lib/apt/lists/*
EOF

# install packages, set locale, add default group
RUN <<-EOF
	chmod a+x /usr/local/bin/apt-get-update-install
	mkdir -p -m 775 /usr/share/man/man1
	apt-get-update-install apt-utils locales wget bzip2 ca-certificates sudo
	localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
	ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime
	echo ${TZ} >/etc/timezone
	groupadd --gid 999 --force docker
EOF

USER 0:999
WORKDIR ${MAMBA_INSTALL_ROOT}

# install micromamba to MAMBA_INSTALL_ROOT/bin
RUN <<-EOF
	platform=$(uname | tr [:upper:] [:lower:])-$(uname -m | sed 's/amd//g' | sed 's/x86_//g')
	# wget -qO- "https://micromamba.snakepit.net/api/micromamba/$platform/latest" | tar -xvj bin/micromamba
	wget -qc "https://anaconda.org/conda-forge/micromamba/0.24.0/download/$platform/micromamba-0.24.0-0.tar.bz2" -O - | tar -xvj bin
	mv -f bin/micromamba bin/_micromamba
EOF

# conda/mamba/micromamba shell activation template
RUN cat <<-EOF >>/etc/profile.d/micromamba.sh
	export MAMBA_EXE="${MAMBA_INSTALL_ROOT}/bin/_micromamba";
	export MAMBA_ROOT_PREFIX="${MAMBA_INSTALL_ROOT}";
	$("${MAMBA_INSTALL_ROOT}/bin/_micromamba" shell hook --shell=bash)
EOF

# for login non-interactive shells
RUN cat <<-"EOF" >>/etc/skel/.bashrc

	# >>> micromamba initialize >>>
	command -v micromamba &>/dev/null || source "/etc/profile.d/micromamba.sh"
	alias conda=micromamba
	alias mamba=micromamba
	# <<< micromamba initialize <<<
EOF

# default conda config file
RUN cat <<-EOF >${MAMBA_INSTALL_ROOT}/.condarc
	envs_dirs:
	  - ~/.conda/envs
	  - ${MAMBA_INSTALL_ROOT}/envs
	channels:
	  - conda-forge
	  - anaconda
	channel_priority: strict
	show_channel_urls: True
	allow_softlinks: False
	pip_interop_enabled: True
	always_yes: True
EOF

# skeleton files and folders for new users
RUN <<-EOF
	mkdir -p /etc/skel/.config /etc/skel/.cache /etc/skel/.conda/envs \
		/etc/skel/.local/share /etc/skel/.local/state /etc/skel/.local/bin \
		/etc/skel/.vscode-server/extensions
	cat /etc/skel/.bashrc | tee -a /root/.bashrc /root/.profile >/dev/null
	cp -f ${MAMBA_INSTALL_ROOT}/.condarc /etc/skel/.conda/.condarc
	chmod a+rx /etc/profile.d/micromamba.sh

	# add a default user (no sudo)
	useradd -u 999 -g 999 --no-log-init -ms /bin/bash djuser
	chown -R 999:999 ${MAMBA_INSTALL_ROOT}
	chmod -R a+rwX,o-w,ug+s,+t,-t ${MAMBA_INSTALL_ROOT}
	chown -R 999:999 /var/log
	chmod -R a+rwX,o-w,ug+s,+t,-t /var/log
EOF

SHELL [ "/bin/bash",  "-elc" ]
USER 999:999
RUN <<-EOF
	# install base python and pip
	micromamba activate
	micromamba install -yvq -c conda-forge "python=${PY_VER}" pip

	# cleanup and management
	micromamba clean -fya
	micromamba update -ya
	mkdir -p ${MAMBA_INSTALL_ROOT}/envs
EOF

USER 0:999
RUN <<-EOF
	# updating base env only allowed for root or owner of history file
	chmod -R a+rwX,o-w,ug+s,+t,-t ${MAMBA_INSTALL_ROOT}
	rm -rf /tmp/*
EOF

SHELL [ "/bin/sh", "-c" ]
ENTRYPOINT [ "/bin/sh", "-c" ]
CMD [ ]

## Stage 2 =============================================================================
## IBL Alyx Image No Apache Web Server Dependencies
## -------------------------------------------------------------------------------------
FROM scratch as devcontainer_build
COPY --from=micromamba_debian / /

ARG TIMEZONE
ARG REPO_NAME

# system environment
ENV LANG=en_US.utf8
ENV LC_ALL=en_US.utf8
ENV LANGUAGE=en_US.utf8
ENV LC_CTYPE=en_US.utf8
ENV TZ=${TIMEZONE}

USER 999:999
WORKDIR /home/djuser/${REPO_NAME}
COPY --chown=999:999 ./ ./
SHELL [ "/bin/bash",  "-elc" ]
ENV RELPATH_DEVCONTAINER=./docker/brain_lab_local/.devcontainer/build
USER 0:999
RUN xargs <${RELPATH_DEVCONTAINER}/requirements/apt_requirements.txt apt-get-update-install

USER 999:999
RUN <<-EOF
	cp -f ${RELPATH_DEVCONTAINER}/settings/.datajoint_config.json ./

	# install conda-specific packages using micromamba ---------------------------------
	micromamba activate
	micromamba install -yq --file ${RELPATH_DEVCONTAINER}/requirements/conda_requirements.txt

	# install packages from pypi using pip ---------------------------------------------
	pip install --no-cache --no-input -vr ${RELPATH_DEVCONTAINER}/requirements/pip_requirements.txt

	# cleanup --------------------------------------------------------------------------
	micromamba clean -fya
	micromamba update -ya
	rm -rf /tmp/*
EOF

## Stage 4 =============================================================================
## Final/Target Devcontainer Image
## -------------------------------------------------------------------------------------
FROM scratch as devcontainer
COPY --from=devcontainer_build / /

# inherit from global args
ARG IMAGE_CREATED
ARG WORKFLOW_VERSION
ARG TIMEZONE
ARG REPO_NAME

# system environment
ENV LANG=en_US.utf8
ENV LC_ALL=en_US.utf8
ENV LANGUAGE=en_US.utf8
ENV LC_CTYPE=en_US.utf8
ENV TZ=${TIMEZONE}

# image labels
LABEL org.opencontainers.image.ref.name="${REPO_NAME}"
LABEL org.opencontainers.image.authors "FirstName LastName"
LABEL org.opencontainers.image.vendor="DataJoint"
LABEL org.opencontainers.image.title "${REPO_NAME}"
LABEL org.opencontainers.image.description "A development container with a debian-based python environment"
LABEL org.opencontainers.image.created="$IMAGE_CREATED"
LABEL org.opencontainers.image.version="$WORKFLOW_VERSION"

WORKDIR /home/djuser/science-institute_brain-lab
USER djuser:docker
SHELL [ "/bin/bash",  "-elc" ]
ENTRYPOINT [ "/bin/bash",  "-elc" ]
CMD [ "tail", "-f", "/dev/null" ]
