FROM registry.access.redhat.com/ubi9/ubi:latest as base

ARG TARGETOS
ARG TARGETARCH

ENV GRAFANA_VERSION=9.4.3
ENV LOKI_VERSION=2.7.4

ADD https://dl.grafana.com/oss/release/grafana-${GRAFANA_VERSION}.${TARGETOS}-${TARGETARCH}.tar.gz /opt
ADD https://github.com/grafana/loki/releases/download/v${LOKI_VERSION}/loki-${TARGETOS}-${TARGETARCH}.zip /opt
ADD https://github.com/grafana/loki/releases/download/v${LOKI_VERSION}/promtail-${TARGETOS}-${TARGETARCH}.zip /opt

RUN tar xf /opt/grafana-${GRAFANA_VERSION}.${TARGETOS}-${TARGETARCH}.tar.gz -C /opt && rm -f /opt/grafana-${GRAFANA_VERSION}.${TARGETOS}-${TARGETARCH}.tar.gz \
    && mv /opt/grafana-${GRAFANA_VERSION} /opt/grafana && mkdir -p /opt/grafana/conf/provisioning/{datasources,dashboards} \
    && mkdir /opt/grafana/dashboards
COPY grafana/grafana.ini /opt/grafana/conf/
COPY grafana/datasources.yml /opt/grafana/conf/provisioning/datasources/
COPY grafana/dashboard_provisioning.yml /opt/grafana/conf/provisioning/dashboards/
COPY grafana/*.json /opt/grafana/dashboards/
RUN dnf install unzip -y \
    && mkdir -p /opt/loki/data && unzip /opt/loki-${TARGETOS}-${TARGETARCH}.zip -d /opt/loki && rm -f /opt/loki-${TARGETOS}-${TARGETARCH}.zip \
    && mkdir /opt/promtail && unzip /opt/promtail-${TARGETOS}-${TARGETARCH}.zip -d /opt/promtail && rm -f /opt/promtail-${TARGETOS}-${TARGETARCH}.zip \
    && find /opt/loki -type f -name "loki-${TARGETOS}-*64" -exec mv {} /opt/loki/loki-server \; \
    && find /opt/promtail -type f -name "promtail-${TARGETOS}-*64" -exec mv {} /opt/promtail/promtail-agent \;
COPY loki/loki-local-config.yaml /opt/loki/
COPY loki/promtail-config* /opt/promtail/
COPY main.py /opt/

FROM registry.access.redhat.com/ubi9/ubi:latest
COPY --from=base /opt /opt
RUN mkdir /logs &&\
	chgrp -R 0 /{opt,logs} &&\
	chmod -R g=u /{opt,logs} 
#USER 1000
EXPOSE 3000 3100
CMD ["python3", "/opt/main.py"]
