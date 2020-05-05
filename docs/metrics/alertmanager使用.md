
# 四：报警

详细的报警见[官方文档](https://prometheus.io/docs/alerting/overview/)

Alertmanage 用于设置 Prometheus 的警报，用于对警报进行去重、分组、然后路由到不同的接收器

Alertmanage 是一个可以集群化的独立警报管理工具


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