


# Prometheus

```shell
# the actual amount of time between target scrapes
prometheus_target_interval_length_seconds

# the per-second rate of chunks being created in the self-scraped Prometheu
rate(prometheus_tsdb_head_chunks_created_total[1m])

```

# CPU 


```shell
# 2 分钟内 CPU 平均使用百分比
(1-((sum(increase(node_cpu_seconds_total{mode="idle"}[2m])) by (instance)) / (sum(increase(node_cpu_seconds_total[2m])) by (instance)))) * 100

# 主机 CPU 数量
count by (instance)(node_cpu_seconds_total{mode="idle"})

# 1分钟平均负载超过主机 CPU 数量的两倍
node_load1 > on (instance) 2 * count by (instance)(node_cpu_seconds_total{mode="idle"})
```



# 内存

```shell
# 内存百分比
(1-((node_memory_MemFree_bytes + node_memory_Cached_bytes +
node_memory_Buffers_bytes) / node_memory_MemTotal_bytes)) * 100

```


# 磁盘

```shell
# 磁盘使用情况
(node_filesystem_size_bytes{mountpoint="/"} - node_filesystem_free_bytes{mountpoint="/"}) / node_filesystem_size_bytes{mountpoint="/"} * 100

# 文件系统是否在接下来四个小时用光
predict_linear(node_filesystem_free_bytes{mountpoint="/"}[1h], 4*3600) < 0
```

- [prometheus 监控之 mysql 篇（含mysql报警规则）](https://blog.csdn.net/qq_25934401/article/details/82594478)

