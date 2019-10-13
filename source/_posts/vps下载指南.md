---
title: vps-aria2下载
date: 2019-10-13 09:29:48
tags: [vps, linux]
---

买了一台罗马尼亚的大盘鸡。
<!--more-->

#### 查看基本情况
```shell
root@master-1:~# df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/simfs      1.0T  111G  914G  11% /
devtmpfs        512M     0  512M   0% /dev
tmpfs           512M     0  512M   0% /dev/shm
tmpfs           512M  6.6M  506M   2% /run

测试带宽：
$ wget https://raw.github.com/sivel/speedtest-cli/master/speedtest.py
$ python speedtest.py
speedtest会选择最近的一个节点进行测试。
列出所有服务器：
$ python speedtest.py --list|more
选择一个服务器测试：
$ python speedtest.py --server 11599

查看架构：
$ apt install virt-what -y
$ virt-what
openvz
```

#### aria2
```shell
$ apt update
$ apt install aria2 -y
```
- 示例：
```shell
$ aria2c http://example.org/mylinux.iso
$ aria2c http://a/f.iso ftp://b/f.iso
Download using 2 connections per host:
$ aria2c -x2 http://a/f.iso
BT
$ aria2c http://example.org/mylinux.torrent
BitTorrent Magnet URI:
$ aria2c 'magnet:?xt=urn:btih:248D0A1CD08284299DE78D5C1ED359BB46717D8C'
Metalink:
$ aria2c http://example.org/mylinux.metalink
Download URIs found in text file:
$ aria2c -i uris.txt
```
man aria2c
