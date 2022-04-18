# syntax=docker/dockerfile:1

ARG PROJECT_NAME=datajoint-workflow-brain
ARG IMPORT_NAME=brainwf
ARG REPO_OWNER=dj-sciops
ARG REPO_NAME=science-institute_brain-lab
ARG HOST_UID=1000
ARG HOST_GID=1000
ARG USER_SUDO=true
ARG IMAGE_DATE=2021-11-11T11:11:11Z
ARG WORKFLOW_VERSION=v0.0.1

# Stage 1 ==============================================================================
# docker build -f devcontainer.Dockerfile --tag wf_img_1 --target build_pyenv ..
# docker run -itd --user root --name wf_build_pyenv wf_img_1 bash
FROM ghcr.io/iamamutt/conda_base:latest as build_pyenv

ARG REPO_NAME
ARG PROJECT_NAME
ARG HOST_GID
WORKDIR /usr/local/src/${REPO_NAME}
COPY ./ ./
SHELL [ "/bin/bash", "-ec" ]

RUN <<-EOF
	cp -f docker/apt_requirements.txt ../apt_requirements.txt
	cp -f docker/.datajoint_config.json ../.datajoint_config.json
	init-apt-deps ../apt_requirements.txt
	init-conda-env environment.yml
	source ~/.bashrc
	conda-run pip install -q '.[dev,doc,test,sciops]'
	conda-run pip uninstall -yq ${PROJECT_NAME}
	CONDA_ENV_USER=base conda-run mamba install -yq conda-pack
	conda-run mamba clean -yqa
	chmod -R 2775 /usr/local
	CONDA_ENV_USER=base conda-run conda pack -n ${CONDA_ENV_USER} -o condaenv.tar.gz
	tar -xzf condaenv.tar.gz -C /usr/local
	source /usr/local/bin/activate
	conda-unpack
	rm -rf /usr/local/src/${REPO_NAME}
	chmod -R g+wX /usr/local
EOF

ENTRYPOINT [ "/bin/sh", "-c" ]
CMD [ "tail", "-f", "/dev/null" ]

# Stage 2 ==============================================================================
# docker build -f devcontainer.Dockerfile --tag wf_img_2 --target install_pyenv ..
# docker run -itd --user root --name wf_install_pyenv wf_img_2 bash
FROM debian:11-slim as install_pyenv

ARG REPO_OWNER
ARG REPO_NAME
ARG HOST_UID
ARG HOST_GID
ARG USER_SUDO

ENV NEW_USER_NAME=${REPO_OWNER}
ENV NEW_USER_GROUP=${REPO_OWNER}
ENV NEW_USER_UID=${HOST_UID}
ENV NEW_USER_GID=${HOST_GID}
ENV NEW_USER_SUDO=${USER_SUDO}
ENV WORKFLOW_DIR=/home/${REPO_OWNER}/${REPO_NAME}

SHELL [ "/bin/bash", "-ec" ]
COPY --from=build_pyenv --chown=${NEW_USER_UID}:${NEW_USER_GID} /usr/local/ /usr/local/

RUN <<-EOF
	[[ ${NEW_USER_SUDO} = true ]] && echo "sudo" >> /usr/local/src/apt_requirements.txt
	init-apt-deps /usr/local/src/apt_requirements.txt
	init-new-user
	mkdir -p "${WORKFLOW_DIR}"
	chown ${NEW_USER_NAME}:${NEW_USER_GROUP} "${WORKFLOW_DIR}" /usr/local
EOF

WORKDIR "${WORKFLOW_DIR}"
COPY --chown=${NEW_USER_NAME}:${NEW_USER_GROUP} ./ ./
USER ${NEW_USER_NAME}:${NEW_USER_GROUP}

RUN <<-EOF
	cp -f /usr/local/src/.datajoint_config.json ../.datajoint_config.json
	mkdir -p ../.vscode-server/extensions ../.vscode-server-insiders/extensions
	chmod -R 755 ../.vscode-server*
	source activate
	conda init -q bash
	pip install -e .
EOF

ENTRYPOINT [ "/bin/sh", "-c" ]
CMD [ "tail", "-f", "/dev/null" ]

# Stage 3 ==============================================================================
# docker build -f devcontainer.Dockerfile --tag wf_img_3 --target devcontainer ..
# docker run -itd --user root --name wf_devcontainer wf_img_3 bash
FROM scratch as devcontainer

COPY --from=install_pyenv / /

ARG IMAGE_DATE
ARG WORKFLOW_VERSION
ARG REPO_OWNER
ARG REPO_NAME

LABEL org.opencontainers.image.authors "Joseph Burling"
LABEL org.opencontainers.image.title "science-institute_brain-lab"
LABEL org.opencontainers.image.description "A development container with a debian-based python environment"
LABEL org.opencontainers.image.version "$WORKFLOW_VERSION"
LABEL org.opencontainers.image.created "$IMAGE_DATE"

USER ${REPO_OWNER}:${REPO_OWNER}
WORKDIR /home/${REPO_OWNER}/${REPO_NAME}

ENTRYPOINT [ "/bin/bash", "-lc" ]
CMD [ "tail", "-f", "/dev/null" ]
