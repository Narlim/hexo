---
title: linux格式化u盘
date: 2019-10-07 11:17:51
tags: linux
---
用几条命令就可以了。
<!--more-->

注意操作之前先备份好数据。
#### 卸载u盘
```shell
sudo umount /dev/sdb
```
#### 格式化u盘
```shell
mkfs.vfat /dev/sdb
```
#### 创建分区
```shell
sudo fdisk /dev/sdb
```
#### 格式化分区
```shell
sudo mkfs.vfat /dev/sdb1
```
之后就可以重新写入数据了。

