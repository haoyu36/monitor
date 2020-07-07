#!/bin/bash
# 拉取最新镜像并推送到个人仓库

set -e

ImageArr=(
    'google/cadvisor:latest'
    'pryorda/vmware_exporter:latest'
    'prom/mysqld-exporter:latest'
    'oliver006/redis_exporter:latest'
    'justwatch/elasticsearch_exporter:latest'
)

ImageRepo="registry.cn-shenzhen.aliyuncs.com/haoyu36"



for Image in ${ImageArr[@]};
do
    echo "========================================"
    echo "==> 正在拉取: ${Image}"
    docker pull ${Image}
    NewImage=${ImageRepo}/${Image##*/}
    docker tag  ${Image} ${NewImage}
    echo "==> 正在推送: ${NewImage}"
    docker push ${NewImage}
done

