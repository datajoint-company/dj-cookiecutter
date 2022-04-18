ARG JHUB_VER=1.4.2
ARG PY_VER={{cookiecutter.python_version}}
ARG DIST=debian

FROM datajoint/djlabhub:${JHUB_VER}-py${PY_VER}-${DIST}

ARG DEPLOY_KEY={{cookiecutter.github_repo}}-deploy.pem
ARG REPO_OWNER={{cookiecutter.github_user}}
ARG REPO_NAME={{cookiecutter.github_repo}}
ARG WORKFLOW_VERSION=main

USER root:anaconda

COPY $DEPLOY_KEY /root/.ssh/sciops_deploy.ssh
COPY --chown=anaconda:anaconda ["pip_requirements.txt*", "apt_requirements.txt*", "conda_requirements.txt*", "nofile.txt", "/tmp/"]

RUN apt-get -y update &&\
	[ -f /tmp/apt_requirements.txt ] && xargs </tmp/apt_requirements.txt apt-get -qq install -y --no-install-recommends &&\
	apt-get autoremove -y &&\
	apt-get clean -y &&\
	install -m 644 /dev/null /root/.ssh/known_hosts &&\
	ssh-keyscan -t rsa -H github.com >>/root/.ssh/known_hosts &&\
	mkdir -p /tmp/${REPO_NAME} &&\
	GIT_SSH_COMMAND="ssh -vvv -i /root/.ssh/sciops_deploy.ssh" git clone --branch ${WORKFLOW_VERSION} --single-branch git@github.com:${REPO_OWNER}/${REPO_NAME}.git /tmp/${REPO_NAME} &&\
	chown -R anaconda:anaconda /tmp/${REPO_NAME} &&\
	cp -f /tmp/${REPO_NAME}/docker/.datajoint_config.json /usr/local/bin/.datajoint_config.json &&\
	cp -fR /tmp/${REPO_NAME}/notebooks /home/ &&\
	cp -f /tmp/${REPO_NAME}/notebooks/README* /home/ &&\
	cp -fR /tmp/${REPO_NAME}/scripts /home/common/ &&\
	chown -R :anaconda /home &&\
	chmod -R 2770 /home &&\
	chmod 664 /tmp/djlab_config.yaml &&\
	conda install -y 'mamba' &&\
	rm -rf /root/.ssh/sciops_deploy.ssh /tmp/apt_requirements.txt /var/lib/apt/lists/* /home/notebooks/README*

# Note: permission issues with djlab module, .ipython folder, ipykernel with custom env.

USER anaconda:anaconda
RUN mamba env create -qv -f /tmp/${REPO_NAME}/environment.yml &&\
	conda run --no-capture-output -n {{cookiecutter.__pkg_import_name}} pip install /tmp/${REPO_NAME}

USER root:anaconda
RUN	conda run --no-capture-output -n {{cookiecutter.__pkg_import_name}} ipython kernel install --name={{cookiecutter.__pkg_import_name}} &&\
	rm -fR /tmp/${REPO_NAME} &&\
	mamba clean -ya

USER anaconda:anaconda
WORKDIR /home/notebooks
