
TODO: 

- [ ] Create a database instead of tutorial-db.datajoint.io
- [ ] x



# Docker environments 

## Codebook 

### Docker Build and Run

Change to the `docker` directory so that the docker build context is the current working directory. Create a `.env` file and the change any variables as necessary, then source those variables for later use.

```bash
cd docker
cat <<-EOF > .env
COMPOSE_PROJECT_NAME={{cookiecutter.__project_name}}
JHUB_VER=1.4.2
PY_VER=3.9
DIST=debian
DEPLOY_KEY={{cookiecutter.github_repo}}-deploy.pem
REPO_OWNER={{cookiecutter.github_user}}
REPO_NAME={{cookiecutter.github_repo}}
WORKFLOW_VERSION={{cookiecutter.pkg_version}}
HOST_UID=1000
EOF
set +a 
source .env
set -a
```

```bash
docker build \
  $(cat .env | while read li; do echo --build-arg ${li}; done | xargs) \
  --file codebook.Dockerfile \
  --tag registry.vathes.com/sciops/codebook-${REPO_NAME}:jhub${JHUB_VER}-py${PY_VER}-${DIST}-${WORKFLOW_VERSION} \
  .
```

```bash
docker run -it \
  --platform linux/amd64 \
  --name {{cookiecutter.__project_name}} \
  --user root \
  registry.vathes.com/sciops/codebook-${REPO_NAME}:jhub${JHUB_VER}-py${PY_VER}-${DIST}-${WORKFLOW_VERSION} \
  bash
```

### Docker Compose 

Will automatically load environment variables from `.env` file. 

```bash 
cd docker
export COMPOSE_PROJECT_NAME={{cookiecutter.__project_name}}
docker-compose -f docker-compose-codebook_env.yml up --build -d
```
