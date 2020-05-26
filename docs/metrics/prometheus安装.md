
# 安装

Prometheus 支持多种安装方式，最简单的是直接使用二进制安装，详见[官网安装文档](https://prometheus.io/docs/prometheus/latest/installation/)。这里是我的安装方式：[haoyu36/monitor](https://github.com/haoyu36/monitor)，本文所有的安装和配置都能在这里找到



使用 k8s 部署使用的 yaml 文件来自于  `coreos/kube-prometheus`，kube-prometheus 结合了 Prometheus Operator 和一系列配置


# 使用

自定义资源对象：

- Prometheus: defines Prometheus deployment
- ServiceMonitor: monitor services，automatically generates scrape configuration
- PodMonitor: monitor pods，automatically generates scrape configuration
- PrometheusRule: Prometheus rule, Both Recording Rule and Alerting Rule
- Alertmanager: defines Alertmanager deployment



# 采集 istio 指标

- [How to collect istio metrics using prometheus operator](https://github.com/coreos/prometheus-operator/issues/2502)
- [istio/installer](https://github.com/istio/installer/tree/master/istio-telemetry/grafana/dashboards)

- [Prometheus Operator 高级配置](https://www.qikqiak.com/post/prometheus-operator-advance/)
- [深度解析Istio telemetry V2](https://zhuanlan.zhihu.com/p/136112888)


- [isito文档：通过 Prometheus 查询度量指标](https://istio.io/zh/docs/tasks/observability/metrics/querying-metrics/)
- [isito文档：默认监控指标](https://preliminary.istio.io/zh/docs/reference/config/policy-and-telemetry/metrics/)


```shell
kubectl create secret generic additional-configs --from-file=prometheus-additional.yaml -n monitoring
```

# 扩展阅读


- [coreos/prometheus-operator](https://github.com/coreos/prometheus-operator)
- [coreos/kube-prometheus](https://github.com/coreos/kube-prometheus)


