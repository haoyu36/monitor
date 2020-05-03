
## cadvisor

docker-compose 部署

```yaml
version: "3.1"
services:
  cadvisor:
    image: google/cadvisor:v0.33.0
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    ports:
      - 8080:8080
    restart: always
```

promethus 配置

```yaml
scrape_configs:
  - job_name: 'cadvisor'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:8080']
```



