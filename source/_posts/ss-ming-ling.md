---
title: 'ss 命令'
date: 2019-06-30 17:58:06
tags: [linux]
published: true
hideInList: false
feature: /post-images/ss-ming-ling.jpg
---
听说ss比netstat快，总结一下基本的用法。
<!-- more -->

显示所有tcp socket：
```shell
$ ss -t -a
State      Recv-Q Send-Q                                Local Address:Port                                                 Peer Address:Port
LISTEN     0      128                                               *:ddi-tcp-1                                                       *:*
LISTEN     0      100                                       127.0.0.1:smtp                                                            *:*
LISTEN     0      128                                               *:28369                                                           *:*
```

显示所有udp socket：
```shell
$ ss -u -a
State      Recv-Q Send-Q                                Local Address:Port                                                 Peer Address:Port
UNCONN     0      0                                                 *:ddi-udp-1                                                       *:*
UNCONN     0      0                                         127.0.0.1:323                                                             *:*
UNCONN     0      0                                                 *:bootpc                                                          *:*
UNCONN     0      0                                                :::19562                                                          :::*
UNCONN     0      0                                                :::14966                                                          :::*
```

显示socket简要信息：
```shell
$ ss -s
Total: 201 (kernel 840)
TCP:   7 (estab 1, closed 1, orphaned 0, synrecv 0, timewait 0/0), ports 0

Transport Total     IP        IPv6
*	  840       -         -
RAW	  0         0         0
UDP	  12        3         9
TCP	  6         4         2
INET	  18        7         11
FRAG	  0         0         0
```

列出每个进程及其监听的端口：
```shell
$ ss -pl | grep LISTEN
u_str  LISTEN     0      128    /tmp/ssh-yVStzow349/agent.25406 927847                * 0                     users:(("sshd",pid=25406,fd=8))
u_str  LISTEN     0      10     /var/run/NetworkManager/private-dhcp 21790                 * 0                     users:(("NetworkManager",pid=2775,fd=15))
u_seq  LISTEN     0      128    /run/udev/control 15910                 * 0                     users:(("systemd-udevd",pid=1630,fd=3),("systemd",pid=1,fd=76))
u_str  LISTEN     0      128    /var/run/docker/metrics.sock 24624                 * 0                     users:(("dockerd",pid=3340,fd=3))
u_str  LISTEN     0      128    /var/run/docker.sock 20286                 * 0                     users:(("dockerd",pid=3340,fd=6),("systemd",pid=1,fd=43))
u_str  LISTEN     0      128    /run/dbus/system_bus_socket 20288                 * 0                     users:(("dbus-daemon",pid=2723,fd=3),("systemd",pid=1,fd=25))

注意：
-n参数：不解析主机名（提升速度）
比如我想查看tomcat监听的端口：
# ss -pl | grep LISTEN
tcp    LISTEN     0      1      127.0.0.1:8005                  *:*                     users:(("java",pid=1,fd=63))
tcp    LISTEN     0      100     *:8009                  *:*                     users:(("java",pid=1,fd=47))
tcp    LISTEN     0      100     *:http-alt              *:*                     users:(("java",pid=1,fd=42))
这个http-alt让人郁闷，我的8080端口呢？

# ss -pln | grep LISTEN
tcp    LISTEN     0      1      127.0.0.1:8005                  *:*                   users:(("java",pid=1,fd=63))
tcp    LISTEN     0      100       *:8009                  *:*                   users:(("java",pid=1,fd=47))
tcp    LISTEN     0      100       *:8080                  *:*                   users:(("java",pid=1,fd=42))
这样就舒服多了。

还有一个相反的-r参数：
# ss -plr | grep LISTEN
tcp    LISTEN     0      1      localhost:8005                  *:*                     users:(("java",pid=1,fd=63))
tcp    LISTEN     0      100     *:8009                  *:*                     users:(("java",pid=1,fd=47))
tcp    LISTEN     0      100     *:http-alt              *:*                     users:(("java",pid=1,fd=42))

所以-n不仅仅是解析主机名，还有端口。
```

查看http并发连接数：
```shell
$ ss  -o state established  '( dport = :http or sport = :http )'
```

端口筛选
```shell
ss dport OP PORT
示例：
ss sport = :80
ss dprot = :http
ss dport \> 1024
ss state connected sport = :http
```
