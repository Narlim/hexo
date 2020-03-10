---
title: debian resolvconf and resolv.conf
date: 2020-03-11 00:36:32
tags: ['debian','dns']
---

debian的dns服务器配置。
<!--more-->

debian的`/etc/resolv.conf`，如果是一个软链接到`/etc/resolvconf/run/resolv.conf`，那么修改`/etc/resolv.conf`是不行的，重启后就会失效，它是被`resolvconf`这个程序控制的。所以要修改的话要改`/etc/network/interfaces`, 添加下面的dns-nameservers配置：

```bash
    gateway 192.168.1.1
    dns-nameservers 192.168.2.1
```

[debian wiki](https://wiki.debian.org/zh_CN/NetworkConfiguration#A.2BYktSqJFNf25jpVPj-)
