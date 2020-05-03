
## 部署

使用 docker-compose 部署 all-in-one，部署 jaeger 最简单使用 all-in-one 镜像

```yaml
version: '3.7'
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "6831:6831/udp"
      - "6832:6832/udp"
      - "16686:16686"
      - "5778:5778"
      - "14268:14268"
```

官方 HotROD 案例

```yaml
version: '3.7'
services:
  hotrod:
    image: jaegertracing/example-hotrod:latest
    ports:
      - "8080:8080"
    command: ["all"]
    environment:
      - JAEGER_AGENT_HOST=xxx
      - JAEGER_AGENT_PORT=6831
```

