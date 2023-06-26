# Variables
APP_NAME := aap-log-visualizer
ARCH ?= amd64
OS ?= linux
CONTAINER_RUNTIME ?= podman
LOGS_PATH ?= "../logs"
# Run tests against code using pylint, flake8, and pytest
tests:
	@pylint --rcfile=.pylintrc *.py && flake8 --max-line-length=100 *.py && pytest
# Build docker image
build:
	@${CONTAINER_RUNTIME} build --build-arg TARGETARCH=${ARCH} --build-arg TARGETOS=${OS} -t ${APP_NAME} .
# Start an aap troubleshooter container
run:
	@${CONTAINER_RUNTIME} rm -f aaplv && ${CONTAINER_RUNTIME} run --name aaplv -d -v ${LOGS_PATH}:/logs:Z -p 3000:3000 localhost/${APP_NAME}
# Container shell for debugging/dev
shell:
	@${CONTAINER_RUNTIME} exec -it aaplv /bin/bash
runshell:
	@${CONTAINER_RUNTIME} run --rm -it -v ${LOGS_PATH}:/logs:Z -p 3000:3000 -p 3100:3100 localhost/${APP_NAME}
# Clean ${CONTAINER_RUNTIME} images
clean:
	@${CONTAINER_RUNTIME} rm -f aaplv && ${CONTAINER_RUNTIME} image prune -af
