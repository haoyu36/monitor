> Prometheus is a new generation of cloud-native monitoring system

# 一：概述

## 1.1 概念

- `TSDB`: 时间序列数据库
- `Metrics`: 时间序列的数值
- `Label`: 健值对，描述时间序列的维度
- `Target`: 执行抓取 Metrics 的来源
- `Job`: 一组具有相同 Target 的集合
- `Instance`: a label that uniquely identifies a target in a job
- `Exporter`: 数据采集组件，暴露 Metrics


## 1.2 架构

![1583759415](http://pic.haoyu95.cn/uploads/big/e06217a5066529c62c8942862bc9493c.png)

`Prometheus` 的架构中主要组件有:

- Prometheus server
- Alertmanager
- Web UI 

`Prometheus Server` 主要负责数据的收集，存储并且对外提供数据查询支持，数据指标的收集使用 Pull 的方式，通过大量的第三方 [Exporter](https://prometheus.io/docs/instrumenting/exporters/) 可以很方便的暴露数据。对于短期运行的临时作业，可以通过 Push 将数据推送到 PushGateway，然后 Prometheus 再通过 Pull 的方式从 PushGateway 获取

除此之外，`Prometheus Server` 还定义告警规则以及产生告警，并将告警发送给 Alertmanager。Alertmanager 组件则处理这些告警，去重、分组、静默等操作，然后通过 Email、Slack、DingDing 等方式发送警报

Prometheus 有一个内置的仪表盘和图形界面，适合调试和构建警报。如果想要更好的可视化界面，构建大量的仪表盘，可以使用 Grafana


## 1.3 存储

Prometheus 是一种基于时间序列 (time series) 的模型， 时间序列是一系列有序的等时间间隔的数据。时间序列数据库是为时间序列数据明确设计的数据库



Prometheus TSDB 在单机上可以支撑每秒百万级的时间序列写入

Prometheus 的性能取决于配置、所搜集时间序列的数量以及服务器上规则的复杂性。Prometheus 会将最新的数据缓存在内存的，所以会有一些的内存消耗，并且每个收集的时间序列、查询和记录规则都会消耗进程内存。如果采集数据较为频繁，会消耗大量的磁盘空间


Prometheus TSDB 默认时序数据每 2h 存储一个 block。每个 block 由一个目录组成。最新写入的数据被保存在内存 block 中，达到2h后写入磁盘。为了防止程序崩溃导致数据丢失，实现了WAL（Write-Ahead-Log）机制。block 保存一定的时间后会被压缩

每个样本通常为 1～2 个字节


## 1.4 高可用

Prometheus 支持多种安装方式，最简单的是使用二进制安装，详见[官网安装文档](https://prometheus.io/docs/prometheus/latest/installation/)。这里是我的安装方式：[haoyu36/monitor](https://github.com/haoyu36/monitor)，本文所有的安装和配置都能在这里找到

Prometheus 单机安装非常方便。但整个系统的吞吐量上限、伸缩性、高可用也会受限于单台服务器

单机无法存储大量的监控数据，可以通过指定远程存储来扩展磁盘，也可以配置联邦集群以让 Prometheus 服务器从另一台 Prometheus 服务器抓取选定的时间序列


# 二：配置

配置文件定义了抓取作业及其实例有关的所有内容，以及哪些规则文件加载，配置文件可以通过热加载更新

Prometheus 配置文件格式为 YAML，启动时通过参数 --config.file 来指定。[官方文档](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)

```yaml
# 指定存储目录
--storage.tsdb.path=/prometheus

# 指定数据保存的时间
--storage.tsdb.retention.time=15d
```

## 2.1 配置文件

配置文件的框架如下：

```yaml
# the Prometheus server's global configuration
global:
  scrape_interval: 15s    # how often Prometheus will scrape targets
  evaluation_interval: 15s    # how often Prometheus will evaluate rules (Recording Rule And Alerting Rule)

# 警报配置
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - alertmanager:9093

# 指定包含记录规则或警报规则的文件列表
rule_files:
  - 'alert.rules'

# what resources Prometheus monitors
scrape_configs:
  # 一组用于相同采集目的的实例，通过一个任务 (Job) 进行管理
  - job_name: 'prometheus'
    scrape_interval: 5s    # 覆盖全局配置
    static_configs:
    - targets:    # 监控目标
        - 'localhost:9090'
      # 为上述 target 追加公共 label
      labels:
        name: haoyu
```

## 2.2 Label

标签名称由 ASCII 字符，数字，以及下划线组成， 其中 __ 开头属于 Prometheus 保留，标签的值可以是任何 Unicode 字符，支持中文

通常时间序列都有一个 instance 标签和一个 job 标签

标签可以定义目标，并为时间序列提供上下文。更改或添加标签会创建新的时间序列

每个指标都自带有两个标签，Instance 和 job，job 是根据抓取作业中的作业名称设置的，一般用于描述正在监控事物的类型，Instance 用于标识目标，通常是目标地址的 IP 和端口


## 2.2 服务发现

当被监控集群的规模较大时，需要使用服务发现的方式处理要监控资源的发现，而不是取手动修改配置文件，服务发现可以是文件，Consul、DNS 等等


```yaml
scrape_configs:
  # 使用文件服务发现的方式
  - job_name: 'node-exporter'
    file_sd_configs:
      - files:
        - targets/nodes.json
```

k8s 的[服务发现机制](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config)



## 2.3 联邦集群

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


## 2.4 Recording Rule

`Recording Rule` 的用以预先计算比较复杂的、执行时间较长的PromQL语句，并将其执行结果保存成一条单独的时序，后续查询时直接返回，可以降低 Prometheus 的响应时间

命名：`level:metric:operations`。level 表示聚合级别，以及规则输出的标签，metric 是指标名称，operations为应用指标的操作列表


```yaml
groups:
    - name: node_rules    # 规则组名，全局唯一
      interval: 30    # 覆盖全局配置
      # 可以定义多条记录规则
      rules:
      - record: instance:node_cpu:avg_rate5m    # 记录规则的名称，即 metric 名称
        # PromQL 语句
        expr: 100 - avg (irate(node_cpu_seconds_total{job="node",mode="idle"}[5m])) by (instance) * 100
        # 标签，追加到新生成的序列中，冲突覆盖
        labels: 
          a: b
```


## 2.5 pushgateway

pushgateway 本身也是一个 http 服务器，使用 pushgateway 可以自定义监控数据



# 三：PromQL

PromQL 是 Prometheus 提供的结构化查询语言，支持Instant vector（瞬时值查询）、Range vector（范围查询）、多种function 以及多种聚合操作

## 3.1 格式

一条 Prometheus 数据由一个 metric 和 N 个 label 组成的，格式为：

`<time series name>{<label name>=<label value>, ...}`

时间序列的名字应该具有语义化，一般表示一个可以度量的指标


Prometheus 启动之后会暴露一些指标，[http://127.0.0.1:9090/metrics](http://127.0.0.1:9090/metrics)，格式为：

![1585133720](http://pic.haoyu95.cn/uploads/big/e279d5d5046f6ee399b86415611fe49c.png)


## 3.2 指标类型

Prometheus 定义了4中不同的指标类型(metric type)：

- Counter: 计数器，只增不减，如请求次数、错误发生次数等等
- Gauge: 仪表盘，一般的数值，随着时间推移而无规则变化，如温度变化、内存使用变化等等
- Histogram: 直方图，对一段时间范围内数据进行采样，如请求耗时、响应大小等等
- Summary: 汇总，根据样本统计百分位


## 3.3 查询语法

详细查询语法见[官方文档](https://prometheus.io/docs/prometheus/latest/querying/basics/)

### 过滤

- -=
- !=
- =~: 模糊匹配
- [3m]: 查询3分钟内的指标，用于 Counter 指标


### 函数

- rate: 计算一定范围内时间序列的每秒平均增长率，只能与 Counter 一起使用，适用于增长很慢的 counter 或用于警报的场景
- irate: 计算的是每秒瞬时增加速率，适用于增长较快的 counter 的瞬时增长率
- increase: 计算一定范围内时间序列的增长总量，用于 Counter 类型
- sum: 求和

# 四：报警

详细的报警见[官方文档](https://prometheus.io/docs/alerting/overview/)

Alertmanage 用于对警报进行去重、分组、然后路由到不同的接收器


## Alerting Rule

`Alerting Rule` 主要用于告警的判定，Alerting Rule 会定义一条PromQL 语句，然后定时执行该PromQL语句并根据执行结果判断是否触发告警

```yaml
groups:
- name: example    # 告警组的名称
  interval: 30    # 覆盖全局配置
  rules:
  # Alert for any instance that is unreachable for >5 minutes.
  - alert: InstanceDown    # 告警名称
    expr: up == 0    # PromQl 语句
    for: 10s    # 告警触发的等待时间
    # 自定义 label
    labels:
      severity: page
    # 告警发生时，会发送 annotations 附加信息，也可以使用模版
    annotations:
      summary: "Instance {{ $labels.instance }} down"
      description: "Alerting: {{ $labels.instance }} of job {{ $labels.job }} has been down for more than 10s minutes."
```


## 报警处理

```yaml
# 警报全局配置
global:
  resolve_timeout: 5m

# 保存警报模版的目录列表
templates:
- 'dingding.tmpl'

# 路由，处理特定的传入警报
route:
  group_by: ['alertname']    # 警报分组的方式
  group_wait: 10s
  group_interval: 10s    # 重复发送警报等待的时间
  repeat_interval: 1h
  receiver: 'DingDing'

# 警报的接收器
receivers:
- name: 'DingDing'
  webhook_configs:
  - url: 'http://192.168.5.214:8060/dingtalk/webhook1/send'
    send_resolved: true

```

警报有三种状态：

- Inactive: 警报未激活
- Pending: 警报已满足测试表达式条件，但仍在等待 for 子句中指定的持续时间
- Firing: 警报已满足测试表达式条件，并且 Pending 时间已超过 for 子句的持续时间



# 五：扩展阅读

## 资料

- [prometheus官方文档](https://prometheus.io/docs/introduction/overview/)
- [实战 Prometheus 搭建监控系统](https://www.aneasystone.com/archives/2018/11/prometheus-in-action.html)
- [roaldnefs/awesome-prometheus](https://github.com/roaldnefs/awesome-prometheus)
- [samber/awesome-prometheus-alerts](https://github.com/samber/awesome-prometheus-alerts/)
- [reliable insights](https://www.robustperception.io/tag/prometheus)

## 高可用

- [thanos-io/thanos](https://github.com/thanos-io/thanos)
- [m3db/m3](https://github.com/m3db/m3)

## 书籍

- prometheus监控实战
