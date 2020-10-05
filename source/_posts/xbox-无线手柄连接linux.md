---
title: xbox 无线手柄连接linux
date: 2020-10-05 13:26:07
tags: [linux, game]
---

xbox的无线手柄连接linux的蓝牙的时候，会有一个小问题。
<!--more-->

因为linux的蓝牙默认是启用的ertm模式，在这个模式下，xbox的手柄是连接不了的，所以有一个解决办法是关闭这个模式：

### 第一个方法
```sh
sudo echo 1 > /sys/module/bluetooth/parameters/disable_ertm
```
然后重启蓝牙：
```sh
systemctl restart bluebooh
```
但是这个办法电脑重启以后就会失效，每次连接都要来一遍就有点麻烦。

### 第二个方法
还有一个一劳永逸的办法就是安装一个第三方的xbox手柄驱动:
[github](https://github.com/atar-axis/xpadneo)

#### 安装
```sh
arch linux：

sudo pacman -S dkms linux-headers bluez bluez-utils

git clone https://github.com/atar-axis/xpadneo.git

cd xpadneo
sudo ./install.sh
```
装完以后重启配对蓝牙就ok了。可以发现，这个项目还提供了一些手柄的高级操作，有一些甚至在windows下面都不支持。