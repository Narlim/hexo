---
title: 'docker swarm集群部署traefik及tls证书'
date: 2019-06-28 21:33:28
tags: [traefik]
published: true
hideInList: false
feature: /post-images/traefik.jpg
---
需要一个swarm集群= = ，我们用traefik的动态配置，所谓的动态配置就是你修改配置文件以后，不用手动重启traefik，只要重启微服务，它会自动发现你的修改并且应用。
<!-- more -->

traefik的那些概念我不讲了，官方文档说得很清楚，我们直接在swarm集群里面起一个traefik：
``` yaml
version: "3.7"
services:
  traefik:
    image: traefik:v1.7-alpine
    ports:
      - 80:80
      - 443:443
    deploy:
      labels:
        - traefik.frontend.rule=Host:traefik.com
        - traefik.enable=true
        - traefik.port=8080
        - traefik.tags=traefik-public
        - traefik.docker.network=multihost
        - traefik.webservice.frontend.entryPoints=https
      replicas: 1
      placement:
        constraints:
          - node.labels.traefik-public.traefik-public-certificates == true
    configs:
      - source: traefik.toml
        target: /etc/traefik/traefik.toml
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    secrets:
      - source: traefik.com.crt
        target: /ssl/traefik.com.crt
      - source: traefik.com.key
        target: /ssl/traefik.com.key
    networks:
      - multihost
    command: >
      --docker
      --docker.swarmMode
      --docker.watch
      --docker.exposedbydefault=false
      --constraints=tag==traefik-public
      --accessLog
      --api

networks:
  multihost:
    external: true
		
configs:
  traefik.toml:
    external: true

secrets:
  traefik.com.crt:
    external: true
  traefik.com.key:
    external: true
```
几个关键点： --docker.exposedbydefault=false，--constraints=tag==traefik-public，前面一个只暴露有标签的服务，后面一个可以用来只暴露有这个标签的服务给对应的traefik实例，对部署多个traefik有帮助。

我们麻烦一点用了docker的secret保存证书，config保存配置，所以先要创建这两个：
traefik.toml:
``` toml
logLevel = "DEBUG"

defaultEntryPoints = ["http", "https"]

[entryPoints]
  [entryPoints.http]
    address = ":80"
    [entryPoints.http.redirect]
      entryPoint = "https"
  [entryPoints.https]
    address = ":443"

  [entryPoints.https.tls]
    [[entryPoints.https.tls.certificates]]
      certFile = "/ssl/traefik.com.crt"
      keyFile = "/ssl/traefik.com.key"
```
我们把http请求都重定向到https。
`docker config create   traefik.toml    traefik.toml`
docker secret 就不写了。
这样就可以部署service了。

---------------

接下来就是动态配置了，比如说我们想访问后端的rabbitmq：
``` yaml
version: "3.4"
services:
  rabbitmq:
    image: rabbitmq:3.7.5-management
    deploy:
      labels:
        - traefik.frontend.rule=Host:rabbitmq.com
        - traefik.enable=true
        - traefik.port=15672
        - traefik.tags=traefik-public
        - traefik.docker.network=multihost
        - traefik.backend.loadbalancer.swarm=true
```
这里我们用docker swarm mode内置的负载均衡，影响不大。
再看一个复杂一点的：
``` yaml
version: "3.4"
services:
  gateway-service:
    image: 
    deploy:
      labels:
        - traefik.api.frontend.rule=Host:traefik-api.com
        - traefik.web-api.frontend.rule=Host:traefik-api.com;PathPrefix:/api/
        - traefik.accounts.frontend.rule=Host:traefik-accounts.com;PathPrefixStrip:/api
        - traefik.enable=true
        - traefik.port=9000
        - traefik.tags=traefik-public
        - traefik.docker.network=multihost
        - traefik.backend.loadbalancer.swarm=true
```
这里有3个frontend，traefik-api.com, traefik-api.com/api/, traefik-accounts.com/api。
都指向同一个后端，gateway-service。
具体配置看官方文档吧，解释得很清楚。

它还有个web页面：
![](https://narlim.github.io/nototaku/post-images/1561740126917.png)
大概就是这个样子= = 
