import os
import requests
import sys
import subprocess
import shutil
import time

grafana_args = [
    "/opt/grafana/bin/grafana-server",
    "-homepath",
    "/opt/grafana",
    "-config",
    "/opt/grafana/conf/grafana.ini",
    "$@",
    "cfg:default.log.mode=console",
]
grafana = subprocess.Popen(grafana_args)

loki_args = [
    "/opt/loki/loki-linux-amd64",
    "--config.file",
    "/opt/loki/loki-local-config.yaml",
]
loki = subprocess.Popen(loki_args)

year = os.environ.get("YEAR")

if year:
    promtail_config = "/opt/promtail/promtail-config-year.yaml"
    add_year = ['python3', '/opt/add-year-to-logs.py', '-y', year]
    subprocess.Popen(add_year).wait()
else:
    promtail_config = "/opt/promtail/promtail-config.yaml"

promtail_args = [
    "/opt/promtail/promtail-linux-amd64",
    "-config.file",
    promtail_config,
]

while True:
    try:
        response = requests.get("http://localhost:3100/ready")
        if response.text.strip() == "ready":
            break
    except Exception:
        time.sleep(10)
        continue

promtail = subprocess.Popen(promtail_args)

try:
    grafana.wait()
    loki.wait()
    promtail.wait()
except KeyboardInterrupt:
    print("\nAAP log visualizer closed!")
