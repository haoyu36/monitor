#!/bin/bash
# 安装 remote_storage_adapter


# remote_storage_adapter 的二进制文件 需要 go build, 详见 https://github.com/prometheus/prometheus/tree/master/documentation/examples/remote_storage/remote_storage_adapter
chmod 777 remote_storage_adapter
/bin/cp -rf remote_storage_adapter /usr/local/bin/


# 设置系统服务
/bin/cp -rfv remote_storage_adapter.service /lib/systemd/system/
systemctl enable remote_storage_adapter.service
systemctl start remote_storage_adapter.service

