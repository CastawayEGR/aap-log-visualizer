Ansible Automation Platform Log Visualizer
=========
[![CI](https://github.com/CastawayEGR/aap-log-visualizer/actions/workflows/ci.yml/badge.svg)](https://github.com/CastawayEGR/aap-log-visualizer/actions/workflows/ci.yml)
[![CD](https://github.com/CastawayEGR/aap-log-visualizer/actions/workflows/cd.yml/badge.svg)](https://github.com/CastawayEGR/aap-log-visualizer/actions/workflows/cd.yml)
[![MIT License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/CastawayEGR/aap-log-visualizer.svg?logoColor=brightgreen)](https://github.com/CastawayEGR/aap-log-visualizer)
[![GitHub last commit](https://img.shields.io/github/last-commit/CastawayEGR/aap-log-visualizer.svg?logoColor=brightgreen)](https://github.com/CastawayEGR/aap-log-visualizer)

Repository for multi-arch all-in-one container images that contains Grafana, Loki, and Promtail with included dashboards to visualize Ansible Automation Platform must-gather and sosreport logs.

Build
------------

Build linux amd64 based image.

~~~
make build
~~~

Build linux arm64 based image.

~~~
make ARCH=arm64 build
~~~

Build image without using make replace ${OS} with linux/darwin and ${ARCH} with arm64/amd64.

~~~
podman build --build-arg TARGETARCH=${ARCH} --build-arg TARGETOS=${OS} -t ${APP_NAME} .
~~~

Run
----------------

Run prebuilt image from Quay.io.

~~~
podman run --name aaplv -d -v ./{must-gather/sosreport}_dir:/logs:Z -p 3000:3000 quay.io/castawayegr/aap-log-visualizer:latest
~~~

Run locally built image using build section from above.

~~~
podman run --name aaplv -d -v ./{must-gather/sosreport}_dir:/logs:Z -p 3000:3000 localhost:/aap-log-visualizer:latest
~~~

License
-------

MIT

Author Information
------------------

This container repo was created by [Michael Tipton](https://ibeta.org).
