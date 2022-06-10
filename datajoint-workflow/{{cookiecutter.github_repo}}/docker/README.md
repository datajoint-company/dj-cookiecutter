# Docker Containers

See [djsciops-cicd](https://github.com/dj-sciops/djsciops-cicd) for more info.

## Pushing an image to the datajoint container repository

- check your remote

```bash
git remote -v
# origin  https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.github_repo}} (fetch)
# origin  https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.github_repo}} (push)
```

- add upstream remote

```bash
git remote add upstream https://github.com/dj-sciops/{{cookiecutter.github_repo}}
# origin  https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.github_repo}} (fetch)
# origin  https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.github_repo}} (push)
# upstream  https://github.com/dj-sciops/{{cookiecutter.github_repo}} (fetch)
# upstream  https://github.com/dj-sciops/{{cookiecutter.github_repo}} (push)
```

- create a local branch from remote upstream/main and switch to it

```bash
git fetch upstream
git switch -c upstream-main upstream/main
```

- push a tag

```bash
git tag 0.1.1 # recreate local tag
git push upstream 0.1.1 # recreate remote tag and trigger CICD
```

- if something went wrong, delete a tag

```bash
git push upstream --delete 0.1.1 # delete remote tag
git tag -d 0.1.1 # delete local tag
```

- switch back to your local main branch

```bash
git switch main
```

## Standard Worker Environment

TODO: add description

## Devcontainer Environment

> **Note**: Make sure to first set the environment variables file `.env` as outlined at the top of this document, otherwise building the docker image will fail.

### VSCode

You can either open to the docker folder directly from vscode and it'll prompt you to open the devcontainer, or use the supplied script below.

```bash
chmod +x docker/.devcontainer/vscode-open-dev-container
docker/.devcontainer/vscode-open-dev-container
```

### Docker Compose

Will automatically load environment variables from `.env` file.

```bash
cd docker/.devcontainer
docker-compose up --detach --force-recreate --remove-orphans --build
```

### Docker Build and Run

Example building one of the stages from the Dockerfile

**Stage**: `micromamba_debian`

```bash
cd docker/.devcontainer/build
PLTARCH=$(uname -m)              # target architecture for platform
MSTARG=micromamba_debian         # multi-stage build target name
IMGTAG=devcontainer:v0.0.1       # image tag
DCNAME=sciops-devcontainer       # container name
DCUSER=ubuntu                    # container user
```

```bash
# build
docker build --platform=linux/${PLTARCH?} --target=$MSTARG --tag=$IMGTAG .

# start container
docker run --rm -itdu "$DCUSER:docker" --name $DCNAME $IMGTAG bash

# execute a command to running container as root
DCID=$(docker ps -aqf "name=$DCNAME")
docker exec -u "root:docker" ${DCID?} chown $DCUSER:docker /usr/local/conda-meta/history

# stop container
docker stop $DCNAME
```
