

# 一：安装

安装之前需要准备两个配置文件，my.cnf 和 mysql_exporter.service，my.cnf 为连接 mysql 的配置，mysql_exporter.service 为系统服务。首先创建 my.cnf 文件

```shell
# my.cnf
[client]
user=root
password=Admin123
port=3306
host=127.0.0.1    # mysql's ip address
```

这里是测试，所以使用的是 root 账号，一般会为 mysql_exporter 单独创建账号

```mysql
GRANT REPLICATION CLIENT, PROCESS ON *.* TO 'exporter'@'%' identified by 'Admin123';
GRANT SELECT ON performance_schema.* TO 'exporter'@'%';
flush privileges;
```

然后创建系统服务

```shell
# mysql_exporter.service
[Unit]
Description=mysqld_exporter

[Service]
ExecStart=/usr/local/bin/mysqld_exporter --config.my-cnf=/etc/mysqld_exporter/my.cnf
ExecReload=/bin/kill -HUP $MAINPID
Type=simple
KillMode=process
Restart=on-failure
RestartSec=42s

[Install]
WantedBy=multi-user.target
```

运行时的参数配置详见[prometheus/mysqld_exporter](https://github.com/prometheus/mysqld_exporter)，最后执行以下命令安装

```shell
#!/bin/bash
# 指定下载版本
version="0.12.1"
exporter_name="mysqld_exporter-${version}.linux-amd64"

# 下载并解压
curl -OL https://github.com/prometheus/mysqld_exporter/releases/download/v${version}/${exporter_name}.tar.gz
tar -xzf ${exporter_name}.tar.gz
chmod 777 ${exporter_name}/mysqld_exporter
cp ${exporter_name}/mysqld_exporter /usr/local/bin/

# 创建配置存放目录
mkdir /etc/mysqld_exporter
cp my.cnf /etc/mysqld_exporter/

# 设置系统服务
cp mysql_exporter.service /lib/systemd/system/
systemctl enable mysql_exporter.service
systemctl start mysql_exporter.service
```

然后访问 `http://<your_ip>:9104/metrics` 就可以看到采集到的指标，最后在 prometheus 增加 job，常用的查看 mysql 的 Grafana Dashboards 的 ID 为 7362


```yaml
scrape_configs:
  - job_name: 'mysql-exporter'
    scrape_interval: 5s
    static_configs:
      - targets: 
        - '<your_ip>:9104'
```


# 二：PromQL

```shell
# 慢查询一分钟内的增长速率
rate(mysql_global_status_slow_queries[1m])
```


# 三：MySQL Alert

```yaml
groups:
    - name: MySQLStatsAlert
      rules:
      - alert: MysqlDown
        expr: mysql_up == 0
        for: 5m
        labels:
          severity: error
        annotations:
          summary: "MySQL down (instance {{ $labels.instance }})"
          description: "MySQL instance is down on {{ $labels.instance }}\n  VALUE = {{ $value }}\n  LABELS: {{ $labels }}"
      - alert: MysqlTooManyConnections
        expr: avg by (instance) (max_over_time(mysql_global_status_threads_connected[5m])) / avg by (instance) (mysql_global_variables_max_connections) * 100 > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "MySQL too many connections (instance {{ $labels.instance }})"
          description: "More than 80% of MySQL connections are in use on {{ $labels.instance }}\n  VALUE = {{ $value }}\n  LABELS: {{ $labels }}"
```



# 扩展阅读

- [构建高大上的MySQL监控平台](https://blog.51cto.com/xiaoluoge/2476375)





