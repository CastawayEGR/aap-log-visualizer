# Variables
APP_NAME := aap-log-visualizer
ARCH ?= amd64
# Build docker image
build:
	@podman build --build-arg TARGETARCH=${ARCH} -t ${APP_NAME} .
# Start an aap troubleshooter container
run:
	@podman rm -f aaplv && podman run --name aaplv -d -v ../logs:/logs:Z -p 3000:3000 localhost/${APP_NAME}
# Container shell for debugging/dev
shell:
	@podman exec -it aaplv /bin/bash
runshell:
	@podman run --rm -it -v ../logs:/logs:Z -p 3000:3000 -p 3100:3100 localhost/${APP_NAME}
# Clean podman images
clean:
	@podman rm -f aaplv && podman image prune -af
