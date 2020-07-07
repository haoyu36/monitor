#!/bin/bash


set -e

git clone https://github.com/percona/mongodb_exporter.git
cd mongodb_exporter/
docker build -t registry.cn-shenzhen.aliyuncs.com/haoyu36/mongodb_exporter:latest .
docker push registry.cn-shenzhen.aliyuncs.com/haoyu36/mongodb_exporter:latest
cd ..
rm -rf mongodb_exporter

