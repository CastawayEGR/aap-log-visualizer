# Variables
app_name := aap-log-visualizer
# Build docker image
build:
	@podman build -t ${app_name} .
# Start a ocp troubleshooter container
run:
	@podman rm -f aaplv && podman run --name aaplv -d -v ../logs:/logs:Z -p 3000:3000 -p 3100:3100 localhost/${app_name}
# Container shell for debugging/dev
shell:
	@podman exec -it aaplv /bin/bash
runshell:
	@podman run --rm -it -v ../logs:/logs:Z -p 3000:3000 -p 3100:3100 localhost/${app_name}
# Clean podman images
clean:
	@podman rm -f ocpt && podman image prune -af
