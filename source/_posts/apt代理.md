---
title: apt代理
date: 2019-12-06 21:23:20
tags: linux
---

让apt使用socks代理，由于apt默认不支持socks代理，所以需要安装tsocks这个小工具。
<!--more-->

#### 安装

```shell
sudo apt install tsocks -y
配置文件在‘/etc/tsocks.conf’，简单地配置一下就可以了。
```

#### 使用

```shell
sudo -s
tsocks apt update -y
exit
```
