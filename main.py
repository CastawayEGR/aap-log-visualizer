import os
import requests
import signal
import sys
import subprocess
import shutil
import time
import glob
from string import Template

def update_promtail_config():
    year = os.environ.get("YEAR")
    if year:
        config_path = "/opt/promtail/promtail-config-year.yaml"
        add_year = ['python3', '/opt/add-year-to-logs.py', '-y', year]
        subprocess.Popen(add_year).wait()
    elif os.path.isdir("/logs/usr/share/zoneinfo"):
        template_path = "/opt/promtail/promtail-config.yaml.template"
        config_path = "/opt/promtail/promtail-config.yaml"
        path_pattern = "/logs/usr/share/zoneinfo/*/*"
        matching_paths = glob.glob(path_pattern)

        for path in matching_paths:
            directory, filename = path.rsplit("/", 2)[-2:]
    
        if directory and filename:
            timezone = f"{directory}/{filename}"

            with open(template_path, "r") as template_file:
                template_content = template_file.read()
            template = Template(template_content)
            new_template = template.safe_substitute(timezone=timezone)
            with open(config_path, "w") as config_file:
                config_file.write(new_template)
    else:
        config_path = "/opt/promtail/promtail-config.yaml"
    return config_path

def start_grafana_server():
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
    return grafana

def start_loki_server():
    loki_args = [
        "/opt/loki/loki-linux",
        "--config.file",
        "/opt/loki/loki-local-config.yaml",
    ]
    loki = subprocess.Popen(loki_args)
    return loki

def start_promtail(promtail_config):
    promtail_args = [
        "/opt/promtail/promtail-linux",
        "-config.file",
        promtail_config,
    ]

    promtail = subprocess.Popen(promtail_args)
    return promtail

def check_ready():
    while True:
        try:
            response = requests.get("http://localhost:3100/ready")
            if response.text.strip() == "ready":
                break
        except Exception:
            time.sleep(10)
            continue

def sigterm_handler(signum, frame):
    print("AAP log visualizer is shutting down!")
    sys.exit(0)

def main():
    grafana = start_grafana_server()
    loki = start_loki_server()

    promtail_config = update_promtail_config()
    promtail = start_promtail(promtail_config)

    signal.signal(signal.SIGTERM, sigterm_handler)

    while True:
        try:
            grafana.wait()
            loki.wait()
            promtail.wait()
        except Exception as e:
            print("An exception occurred:", str(e))
            sys.exit(1)

if __name__ == "__main__":
    main()
