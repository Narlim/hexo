---
title: linux普通用户切换root
date: 2019-10-11 16:29:45
tags: linux
---
记一次sudo配置的坑。
<!--more-->
下面是当时的sudo配置，在sudoers.d目录下：
```shell
lhadmin ALL=(ALL)   NOPASSWD:ALL,!/bin/su,!/bin/passwd,!/usr/sbin/visudo
```
现在我是lhadmin用户，接着我执行，切换到随便组都可以，不一定是docker：
```shell
sudo newgrp docker
```
用户变成root。😂
后来发现：
```shell
sudo bash
```
直接root，连组也变成root。。索然无味
