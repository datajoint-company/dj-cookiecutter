# Docker Containers

Create a `.env` file and the change any variables as necessary, then source those variables for later use.

```bash
cat <<-EOF > ./docker/.env
COMPOSE_PROJECT_NAME=sciops-brain-lab
JHUB_VER=1.4.2
PY_VER=3.9
DIST=debian
DEPLOY_KEY=science-institute_brain-lab-deploy.pem
REPO_OWNER=dj-sciops
REPO_NAME=science-institute_brain-lab
WORKFLOW_VERSION=v0.0.1
HOST_UID=1000
HOST_GID=1000
DJ_HOST=host.docker.internal
DJ_USER=root
DJ_PASS=simple
EOF
set +a
source .env
set -a
```

## CodeBook Environment

### Docker Build and Run

Change to the `docker` directory so that the docker build context is the current working directory.

```bash
cd docker
docker build \
  $(cat .env | while read li; do echo --build-arg ${li}; done | xargs) \
  --file codebook.Dockerfile \
  --tag registry.vathes.com/${REPO_OWNER}/codebook-${REPO_NAME}:jhub${JHUB_VER}-py${PY_VER}-${DIST}-${WORKFLOW_VERSION} \
  .
```

```bash
docker run -it \
  --platform linux/amd64 \
  --name sciops-brain-lab \
  --user root \
  registry.vathes.com/${REPO_OWNER}/codebook-${REPO_NAME}:jhub${JHUB_VER}-py${PY_VER}-${DIST}-${WORKFLOW_VERSION} \
  bash
```

### Docker Compose

Will automatically load environment variables from `.env` file.

```bash
cd docker
docker-compose -f docker-compose-codebook_env.yaml up --detach --force-recreate --remove-orphans --build
```

## Standard Workflow Environment

### Docker Compose

Will automatically load environment variables from `.env` file.

```bash
cd docker
docker-compose -f docker-compose-standard_workflow.yaml up --detach --force-recreate --remove-orphans --build
```

## Devcontainer Environment

### VSCode

You can either open to the docker folder directly from vscode and it'll prompt you to open the devcontainer, or use the supplied script below. 

```bash
chmod +x docker/.devcontainer/vscode-open-dev-container
docker/.devcontainer/vscode-open-dev-container
```

### Docker Compose

Will automatically load environment variables from `.env` file.

```bash
cd docker
docker-compose -f docker-compose-devcontainer_env.yaml up --detach --force-recreate --remove-orphans --build
```
