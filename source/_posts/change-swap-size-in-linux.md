---
title: change swap size in linux
date: 2020-02-29 16:08:54
tags: linux
---

内存太小了，只能用swap来顶替了。。
<!--more-->

## 几条命令就好了

```bash
$ sudo swapoff -a

$ sudo dd if=/dev/zero of=/swapfile bs=1G count=8
if = input file
of = output file
bs = block size
count = multiplier of blocks

$ sudo mkswap /swapfile

$ sudo swapon /swapfile

$ grep SwapTotal /proc/meminfo
```