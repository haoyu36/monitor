


```shell
node_exporter --collector.textfile.directory="."
```


node_exporter 在这里下载 [prometheus/node_exporter](https://github.com/prometheus/node_exporter)


监控：CPU、内存、磁盘、可用性

node_exporter 可以用于采集主机的指标，启动后默认在 9100 端口运行，并在路径 /metrics 上暴露指标。使用 node_exporter 时可以指定一些收集器，如 textfile 收集器

textfile 收集器可以暴露自定义指标，通过扫描指定目录中的文件，提取所有格式为 Prometheus 指标的字符串，然后暴露以便抓取


