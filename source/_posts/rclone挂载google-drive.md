---
title: rclone挂载google-drive
date: 2019-10-12 23:17:04
tags: [rclone, google drive] 
---

rclone是一个命令行工具用来在云存储之间同步文件。
<!--more-->

#### 安装
Linux/macOS/BSD
```shell
curl https://rclone.org/install.sh | sudo bash
```

#### 配置google drive
```shell
rclone config
（配置完以后也可以用这个命令查看）
```
按照提示来选择就好了。

#### 挂载
```shell
mkdir google-drive
rclone mount remote:path/to/files /path/to/local/mount
或者直接挂载整个云盘
rclone mount google-drive:/ ~/google-drive 
```

#### 移动文件
```shell
rclone move source:path dest:path [flags]
例如：
rclone move -P file google-drive:/root --transfers=1
-P：--progress
--transfers: 并行传输的文件数目，默认为4，内存较小的话改为1
```
还有其他命令用到再说吧。

#### 卸载
```shell
# Linux
fusermount -u /path/to/local/mount
# OS X
umount /path/to/local/mount
```
