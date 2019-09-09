---
title: 'kubenetes滚动升级'
date: 2019-07-06 11:04:18
tags: [kubernetes]
published: true
hideInList: false
feature: /post-images/kubenetes-rolling-update.jpg
---

尝试一下k8s自带的滚动升级。
<!-- more -->

其他的就不讲了，直接记录一下我的操作。
先把k8s的配置文件放上来：
tomcat-service.yaml: 
``` YAML
---
apiVersion: v1
kind: Service
metadata:
  name: tomcat-service
  labels:
    k8s-app: tomcat-service
spec:
  ports:
  - port: 8080
    targetPort: 8080
    protocol: TCP
    name: http
  selector:
    k8s-app: tomcat-service
---
apiVersion: v1
kind: Deployment
metadata:
  name: tomcat-service
spec:
  replicas: 3
  template:
    metadata:
      labels:
        k8s-app: tomcat-service
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: tomcat-service
        image: tomcat:7
        ports:
        - containerPort: 8080
```
ingress.yaml
```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: host-based-ingress
spec:
  rules:
  - host: tomcat.com
    http:
      paths:
      - backend:
          serviceName: tomcat-service
          servicePort: 8080
```
部署到k8s，把hosts文件改一下。

接下来是这样的，不停地请求这个deployment，k8s会把我们的请求负载到3个pod，然后我们部署滚动升级，看看请求是否会出现中断，来验证可用性。
```shell
$ while : ; do curl --connect-timeout 1  -m 2  tomcat.com -I ; sleep 0.5 ;done
```
下面是升级的命令：
```shell
$ kubectl set image deployment/tomcat  tomcat=tomcat:9.0.20
```
结果是会有一到两个请求失败，原因是tomcat启动的时候需要时间，而k8s在tomcat启动的时候就把流量导入了新的pod。这样就不好，那么我们需要用一个ReadinessProbe来告诉k8s我们的pod准备好了：
```yaml
apiVersion: v1
kind: Deployment
metadata:
  name: tomcat-service
spec:
  replicas: 3
  template:
    metadata:
      labels:
        k8s-app: tomcat-service
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: tomcat-service
        image: tomcat:7
        ports:
        - containerPort: 8080
        readinessProbe:
          exec:
            command:
            - rm -f index.html;wget localhost:8080 && grep tomcat index.html
          initialDelaySeconds: 10
          periodSeconds: 5
```
用一个命令来检测tomcat准备好了，而且设置了延迟10s。
```shell
$ kubectl set image deployment/tomcat  tomcat=tomcat:9.0.20
```

下面是结果：
```shell
HTTP/1.1 200
Server: nginx/1.15.6
Date: Thu, 04 Jul 2019 07:32:01 GMT
Content-Type: text/html;charset=UTF-8
Connection: keep-alive
Vary: Accept-Encoding

HTTP/1.1 200 OK
Server: nginx/1.15.6
Date: Thu, 04 Jul 2019 07:32:01 GMT
Content-Type: text/html;charset=ISO-8859-1
Connection: keep-alive
Vary: Accept-Encoding

HTTP/1.1 200
Server: nginx/1.15.6
Date: Thu, 04 Jul 2019 07:32:02 GMT
Content-Type: text/html;charset=UTF-8
Connection: keep-alive
Vary: Accept-Encoding

HTTP/1.1 200 OK
Server: nginx/1.15.6
Date: Thu, 04 Jul 2019 07:32:02 GMT
Content-Type: text/html;charset=ISO-8859-1
Connection: keep-alive
Vary: Accept-Encoding

HTTP/1.1 200
Server: nginx/1.15.6
Date: Thu, 04 Jul 2019 07:32:03 GMT
Content-Type: text/html;charset=UTF-8
Connection: keep-alive
Vary: Accept-Encoding
```
在更新pod的时候发现charset这个参数，tomcat版本不同是不一样的，说明这里在更新pod，而且没有出现请求异常。那么在部署的时候应该能提供零停机。❤️
