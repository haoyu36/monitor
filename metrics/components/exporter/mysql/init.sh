#!/bin/bash
# 安装 mysqld exporter

# 指定下载版本
version="0.12.1"
exporter_name="mysqld_exporter-${version}.linux-amd64"

# 下载并解压
curl -OL https://github.com/prometheus/mysqld_exporter/releases/download/v${version}/${exporter_name}.tar.gz
tar -xzf ${exporter_name}.tar.gz
chmod 777 ${exporter_name}/mysqld_exporter
/bin/cp -rf ${exporter_name}/mysqld_exporter /usr/local/bin/

# 创建配置存放目录
mkdir /etc/mysqld_exporter
/bin/cp -rf my.cnf /etc/mysqld_exporter/

# 设置系统服务
/bin/cp -rf mysql_exporter.service /lib/systemd/system/
systemctl enable mysql_exporter.service
systemctl start mysql_exporter.service
