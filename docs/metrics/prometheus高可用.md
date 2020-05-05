

# 概述

## 1.1 存储

Prometheus 是一种基于时间序列 (time series) 的模型， 时间序列是一系列有序的等时间间隔的数据。时间序列数据库是为时间序列数据明确设计的数据库

Prometheus TSDB 在单机上可以支撑每秒百万级的时间序列写入

Prometheus 的性能取决于配置、所搜集时间序列的数量以及服务器上规则的复杂性。Prometheus 会将最新的数据缓存在内存的，所以会有一些的内存消耗，并且每个收集的时间序列、查询和记录规则都会消耗进程内存。如果采集数据较为频繁，会消耗大量的磁盘空间


Prometheus TSDB 默认时序数据每 2h 存储一个 block。每个 block 由一个目录组成。最新写入的数据被保存在内存 block 中，达到2h后写入磁盘。为了防止程序崩溃导致数据丢失，实现了WAL（Write-Ahead-Log）机制。block 保存一定的时间后会被压缩

每个样本通常为 1～2 个字节


## 1.2 高可用

Prometheus 单机安装非常方便。但整个系统的吞吐量上限、伸缩性、高可用也会受限于单台服务器

单机无法存储大量的监控数据，可以通过指定远程存储来扩展磁盘，也可以配置联邦集群以让 Prometheus 服务器从另一台 Prometheus 服务器抓取选定的时间序列



# 联邦集群

联合集群可以让 Prometheus 服务器从另一台 Prometheus 服务器抓取选定的时间序列

```yaml
scrape_configs:
  - job_name: 'federate'
    scrape_interval: 15s

    honor_labels: true
    metrics_path: '/federate'    # Prometheus 服务器的端点

    # 需要指定要公开的系列
    params:
      'match[]':
        - '{job="prometheus"}'
        - '{__name__=~"job:.*"}'

    static_configs:
      - targets:
        - 'source-prometheus-1:9090'
```

- [官方联邦集群文档](https://prometheus.io/docs/prometheus/latest/federation/)

# 扩展阅读

- [thanos-io/thanos](https://github.com/thanos-io/thanos)
- [m3db/m3](https://github.com/m3db/m3)
