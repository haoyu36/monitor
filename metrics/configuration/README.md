


# prometheus 指标

```shell
# 最后一分钟添加的每秒样本率
rate(prometheus_tsdb_head_samples_appended_total[1m])

# 所有匹配的指标的计数和
sum(count by (__name__)({__name__=~".+"}))

# 进程的内存使用情况
process_resident_memory_bytes
```


## 3.5 常用查询

```bash
# metric 的 http 请求数量
promhttp_metric_handler_requests_total
sum(promhttp_metric_handler_requests_total)    # 汇总
sum(promhttp_metric_handler_requests_total) by (job)   # 按标签维度聚合
sum(rate(promhttp_metric_handler_requests_total[5m])) by (job)    # 速率
```


