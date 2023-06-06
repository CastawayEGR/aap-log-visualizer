FROM ubi9/ubi:latest as base

ENV GRAFANA_VERSION=9.4.3
ENV LOKI_VERSION=2.7.4

ADD https://dl.grafana.com/oss/release/grafana-${GRAFANA_VERSION}.linux-amd64.tar.gz /opt
ADD https://github.com/grafana/loki/releases/download/v${LOKI_VERSION}/loki-linux-amd64.zip /opt
ADD https://github.com/grafana/loki/releases/download/v${LOKI_VERSION}/promtail-linux-amd64.zip /opt

RUN tar xf /opt/grafana-${GRAFANA_VERSION}.linux-amd64.tar.gz -C /opt && rm -f /opt/grafana-${GRAFANA_VERSION}.linux-amd64.tar.gz \
    && mv /opt/grafana-${GRAFANA_VERSION} /opt/grafana && mkdir -p /opt/grafana/conf/provisioning/{datasources,dashboards} \
    && mkdir /opt/grafana/dashboards
COPY grafana/grafana.ini /opt/grafana/conf/
COPY grafana/datasources.yml /opt/grafana/conf/provisioning/datasources/
COPY grafana/dashboard_provisioning.yml /opt/grafana/conf/provisioning/dashboards/
COPY grafana/*.json /opt/grafana/dashboards/
RUN dnf install unzip -y \
    && mkdir -p /opt/loki/data && unzip /opt/loki-linux-amd64.zip -d /opt/loki && rm -f /opt/loki-linux-amd64.zip \
    && mkdir /opt/promtail && unzip /opt/promtail-linux-amd64.zip -d /opt/promtail && rm -f /opt/promtail-linux-amd64.zip
COPY loki/loki-local-config.yaml /opt/loki/
COPY loki/promtail-config.yaml /opt/promtail/
COPY loki/promtail-config-year.yaml /opt/promtail/
COPY main.py /opt/
COPY add-year-to-logs.py /opt/

FROM ubi9/ubi:latest
COPY --from=base /opt /opt
RUN mkdir /metrics && mkdir /logs 
EXPOSE 3000 9090 3100
CMD ["python3", "/opt/main.py"]
