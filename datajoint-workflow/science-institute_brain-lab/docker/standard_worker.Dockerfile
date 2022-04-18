FROM datajoint/djbase:latest

USER root
RUN apt update &&\
	apt-get install -y ssh git

USER anaconda:anaconda
ARG DEPLOY_KEY
COPY --chown=anaconda $DEPLOY_KEY $HOME/.ssh/sciops_deploy.ssh
WORKDIR $HOME
RUN ssh-keyscan github.com >> ~/.ssh/known_hosts &&\
	GIT_SSH_COMMAND="ssh -i $HOME/.ssh/sciops_deploy.ssh"\
	git clone git@github.com:dj-sciops/science-institute_brain-lab.git

RUN cd "$HOME/science-institute_brain-lab" &&\
	pip install '.[sciops]'
