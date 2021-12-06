---
title: NetworkManager 使用
date: 2021-11-25 22:13:55
tags: ['centos', 'network']
---

NetworkManager 是红帽官方推荐的一个网络配置软件，用来代替老的网络配置脚本。这里介绍一些基本的网络配置命令，来完成静态ip配置以及网络连接的管理。

<!--more-->
### 前言
centos7 系统安装完成之后，默认启用 NetworkManager ，但是同时也支持老的脚本管理方式，脚本可以通过：`systemctl cat network.service` 来查看：

NetworkManager 会读取 /etc/sysconfig/network-scripts/ 目录下面的配置文件，这是为了兼容，也可以直接用它自带的 nmcli 命令行配置。

还有两个概念需要明确，connection 和 device；device 很好理解，就是设备，在这里就是网卡，实体网卡或者虚拟玩卡都可以；connection 我们可以将为一个设备配置多个连接，就像一个无线网卡能连接到不同的 WIFI 信号，这里的 WIFI 信号就是 connection.

## 直接用 nmcli 管理
我们拿到一台机器，网卡设备一般都会有，而且第一个设备的名字都会是 eth0 ，那么就可以直接创建一个连接：
```bash
先启动 NetworkManager
systemctl start NetworkManager

创建一个连接：
nmcli c add type ethernet con-name CNNCT1 ifname eth0 ipv4.addr 192.168.1.100/24 ipv4.gateway 192.168.1.1 ipv4.dns 198.168.1.1 ipv4.method manual

默认启用了ipv6,如果没有ipv6的路由，可以关闭：
nmcli c CNNCT1 modify ipv6.method "disabled"

直接 up 就会生效（当你配置了多个连接，也可以用这个命令来切换连接）：
nmcli c up CNNCT1

如果你还想在这个连接上添加策略路由：
nmcli c modify CNNCT1 ipv4.routes "10.0.0.0/24 192.168.1.2 table=100" ipv4.routing-rules "priority 5 fwmark1 table 100"
上面的命令添加了一条源地址为 10.0.0.0 网段的路由，还有一条优先级为 5 的ip rule；因为直接用 ip 命令的话，机器重启配置就没了，所以这样更好。
```
注意： 上面的命令可能 centos7 版本的 NetworkManager 版本并不支持。

## 修改配置文件
对于 centos7 也直接修改配置文件，目录在 /etc/sysconfig/network-scripts/
```bash
vim ifcfg-eth0
BOOTPROTO=static
ONBOOT=yes
IPADDR=192.168.1.73
GATEWAY=192.168.1.1
NETMASK=255.255.255.0
DNS1=8.8.8.8

这里是一些基本的配置，然后
nmcli c reload
nmcli con down eth0
nmcli con up eth0
配置生效
```

如果你不想用 NetworkManager， 那么修改配置文件以后，直接 `systemctl restart network`.

## nmcli 的基本命令
```bash
connection

nmcli c delete <c_name>

nmcli c show <c_name>

device

nmcli d show

nmcli d connect <d_name>

nmcli n
```