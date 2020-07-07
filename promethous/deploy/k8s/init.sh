#!/bin/bash
# 拉取最新的 manifests 并修改


git clone https://github.com/coreos/kube-prometheus.git
cp -r kube-prometheus/manifests .
cd manifests


ImageRepo="registry.cn-shenzhen.aliyuncs.com/haoyu36"


sed -i 's@quay.io/coreos/prometheus-operator.*@'${ImageRepo}'/prometheus-operator:v0.38.0@g' setup/prometheus-operator-deployment.yaml
sed -i 's@jimmidyson/configmap-reload.*@'${ImageRepo}'/configmap-reload:v0.3.0@g' setup/prometheus-operator-deployment.yaml
sed -i 's@quay.io/coreos/prometheus-config-reloader.*@'${ImageRepo}'/prometheus-config-reloader:v0.38.0@g' setup/prometheus-operator-deployment.yaml
sed -i 's@quay.io/coreos/kube-rbac-proxy.*@'${ImageRepo}'/kube-rbac-proxy:v0.4.1@g' setup/prometheus-operator-deployment.yaml

sed -i 's@quay.io/prometheus/prometheus.*@'${ImageRepo}'/prometheus:v2.15.2@g' prometheus-prometheus.yaml
sed -i 's@quay.io/prometheus/alertmanager.*@'${ImageRepo}'/alertmanager:v0.20.0@g' alertmanager-alertmanager.yaml
sed -i 's@quay.io/coreos/k8s-prometheus-adapter-amd64.*@'${ImageRepo}'/k8s-prometheus-adapter-amd64:v0.5.0@g' prometheus-adapter-deployment.yaml
sed -i 's@grafana/grafana.*@'${ImageRepo}'/grafana:6.6.0@g' grafana-deployment.yaml
sed -i 's@quay.io/coreos/kube-state-metrics.*@'${ImageRepo}'/kube-state-metrics:v1.9.5@g' kube-state-metrics-deployment.yaml
sed -i 's@quay.io/coreos/kube-rbac-proxy.*@'${ImageRepo}'/kube-rbac-proxy:v0.4.1@g' kube-state-metrics-deployment.yaml node-exporter-daemonset.yaml
sed -i 's@quay.io/prometheus/node-exporter.*@'${ImageRepo}'/node-exporter:v0.18.1@g' node-exporter-daemonset.yaml


mkdir alertmanager grafana kube-state-metrics node-exporter prometheus
mv alertmanager-* alertmanager/
mv grafana-* grafana/
mv kube-state-metrics-* kube-state-metrics/
mv node-exporter-* node-exporter/
mv prometheus-* prometheus/
