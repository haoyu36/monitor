#!/bin/bash
# 安装 node exporter

# 指定下载版本
version="0.18.1"
exporter_name="node_exporter-${version}.linux-amd64"

# 下载并解压
curl -OL https://github.com/prometheus/node_exporter/releases/download/v${version}/${exporter_name}.tar.gz
tar -xzf ${exporter_name}.tar.gz
chmod 777 ${exporter_name}/node_exporter
/bin/cp -rf${exporter_name}/node_exporter /usr/local/bin/

# 设置系统服务
/bin/cp -rf node_exporter.service /lib/systemd/system/
systemctl enable node_exporter.service
systemctl start node_exporter.service
