#!/bin/bash
# 安装 redis exporter

# 指定下载版本
version="v1.5.2"
exporter_name="redis_exporter-${version}.linux-amd64"

# 下载并解压
curl -OL https://github.com/oliver006/redis_exporter/releases/download/${version}/${exporter_name}.tar.gz
tar -xzf ${exporter_name}.tar.gz
chmod 777 ${exporter_name}/redis_exporter
/bin/cp -rf ${exporter_name}/redis_exporter /usr/local/bin/

# 设置系统服务
/bin/cp -rf redis_exporter.service /lib/systemd/system/
systemctl enable redis_exporter.service
systemctl start redis_exporter.service
