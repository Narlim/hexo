---
title: arch无线网卡配置
date: 2020-05-10 11:28:35
tags: [linux, arch]
---

突然发现买的intel nuc支持无线网卡（之前一直没发现。。。
简单的配置一下，以防没有有线可用的情况下，不至于太尴尬。
<!--more-->

### 查看设备状态：
```bash
lspci -k
```
如果里面有显示，则说明无线网卡驱动已经安装。

手动设置：
需要的包：iw, wpa_supplicant

几个常用命令：
```bash
iw dev

iw dev wlan0 link
```

### 启动网卡：
```bash
ip link set wlan0 up
ip link show wlan0
```

我用的是静态ip：
```bash
ip addr add 192.168.2.112/24 dev wlan0
```
由于用的透明代理，网关由systemd-networkd管理，所以路由这里不需要加。


### 查找接入点(wifi信号):
```bash
iw dev wlan0 scan | less
```
根据SSID找到要连接的wifi

如果wifi的加密方式是WPA/WPA2（一般都是）根据下面的方式关联wifi信号：
```bash
wpa_supplicant -B -i wlan0 -c <(wpa_passphrase your_SSID you_key)  # 这条命令要切到root用户
iw dev wlan0 link
```

### 接下来是网络配置：
由于我是用systemd-networkd来管理，如果是其他的话，可以参考wiki
```bash
vim /etc/systemd/network/20-wireless.network
[Match]
Name=wlp6s0

[Network]
Address=192.168.2.112/24
Gateway=192.168.2.237
DNS=192.168.2.237
```

重启systemd-networkd:
```bash
systemctl restart systemd-networkd
```