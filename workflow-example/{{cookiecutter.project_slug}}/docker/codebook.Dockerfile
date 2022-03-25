## docker build --build-arg DEPLOY_KEY={{ cookiecutter.project_slug }}-deploy.pem --build-arg REPO_NAME={{ cookiecutter.project_slug }} -f codebook.Dockerfile -t registry.vathes.com/sciops/codebook-{{ cookiecutter.project_slug }}:v0.0.0 .

## Single Stage 
FROM datajoint/djlabhub:1.4.2-py3.8-debian

USER root
RUN apt-get -y update && apt-get install -y ssh git
USER anaconda:anaconda

ARG DEPLOY_KEY
COPY --chown=anaconda $DEPLOY_KEY $HOME/.ssh/sciops_deploy.ssh

ARG REPO_NAME
WORKDIR /tmp
RUN ssh-keyscan github.com >> $HOME/.ssh/known_hosts && \
    GIT_SSH_COMMAND="ssh -i $HOME/.ssh/sciops_deploy.ssh" \
    git clone git@github.com:dj-sciops/${REPO_NAME}.git && \
    pip install ./${REPO_NAME} && \
    cp -r ./${REPO_NAME}/notebooks/ /home/ && \
    cp -r ./${REPO_NAME}/images/ /home/notebooks/ && \
    cp ./${REPO_NAME}/README.md /home/notebooks/ && \
    rm -rf /tmp/${REPO_NAME} && \
    rm -rf $HOME/.ssh/sciops_deploy.ssh
WORKDIR /home/notebooks