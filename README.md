Ansible Automation Platform Log Visualizer
=========
[![AAP Log Visualizer CI/CD](https://github.com/CastawayEGR/aap-log-visualizer/actions/workflows/build.yml/badge.svg)](https://github.com/CastawayEGR/aap-log-visualizer/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/CastawayEGR/aap-log-visualizer.svg?logoColor=brightgreen)](https://github.com/CastawayEGR/aap-log-visualizer)
[![GitHub last commit](https://img.shields.io/github/last-commit/CastawayEGR/aap-log-visualizer.svg?logoColor=brightgreen)](https://github.com/CastawayEGR/aap-log-visualizer)

Repository for a multi-arch container image that contains Grafana, Loki, and Promtail to visualize Ansible Automation Platform must-gathers and sosreports.

Build
------------

Build amd64 based image.

~~~
make build
~~~

Build arm64 based image.

~~~
make ARCH=arm64 build
~~~

Run
----------------

~~~
podman run --name aaplv -d -v ./{must-gather/sosreport}_dir:/logs:Z -p 3000:3000 localhost:/aap-log-visualizer:latest
~~~

License
-------

MIT/BSD

Author Information
------------------

This container repo was created by [Michael Tipton](https://ibeta.org).
