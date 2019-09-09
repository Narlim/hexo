---
title: 'wireguard初体验'
date: 2019-07-17 20:09:15
tags: []
published: true
hideInList: false
feature: /post-images/wireguard-chu-ti-yan.jpg
---

WireGuard被视为下一代VPN协议，用来替代OpenVPN，IPSec等VPN协议。
<!-- more -->

### 安装
我就按照官方的quick start来写了。😂
先是服务器端(centos)：
```shell
$ yum update -y
$ sudo curl -Lo /etc/yum.repos.d/wireguard.repo https://copr.fedorainfracloud.org/coprs/jdoss/wireguard/repo/epel-7/jdoss-wireguard-epel-7.repo
$ sudo yum install epel-release
$ sudo yum install wireguard-dkms wireguard-tools

装完之后试一下这个命令：
ip link add dev wg0 type wireguard
如果没有报错就ok了，如果有报错可能是linux-headers没有装什么的。
```
接下来是步骤，服务端和客户端步骤基本一样，也就是操作下面两次（比如我有两台服务器，ip分别为192.168.2.1，192.168.2.2，那么只要改ip和pubkey就可以了）：
```shell
$ wg genkey > private
$ wg pubkey < private
$ ip link add dev wg0 type wireguard
$ wg set wg0 private-key ./private
$ ip addr add 192.168.2.2/24 dev wg0(给这个虚拟网卡一个ip)
$ ip link set wg0 up
$ wg set peer mDSvO/2BLLw7VL8vBEjv0+03RZENksSM/9gxASSxzGQ= allowed-ips 192.168.2.1/32 endpoint 98.142.141.74:36563 (前面为对方的pubkey，endpoint为公网ip)

[root@host ~]# wg
interface: wg0
  public key: mDSvO/2BLLw7VL8vBEjv0+03RZENksSM/9gxASSxzGQ=
  private key: (hidden)
  listening port: 36563

peer: HtQ40EZqljZp4X1u7gvv3bH9W3s5OYG3VHKPlppBuAg=
  endpoint: 58.101.53.63:45896
  allowed ips: 192.168.2.2/32
  latest handshake: 10 seconds ago
  transfer: 105.35 MiB received, 662.53 MiB sent

wg命令可以看到已经连接。
我们在192.178.2.2
ping 192.168.2.1
发现成功。
但是我们并不能直接就可以科学上网。😏
```
默认情况下wg0这个网卡，服务器重启以后就会删除，我们需要保存它的配置：
```shell
$ wg showconf wg0 > /etc/wireguard/wg0.conf
加载：
$ wg setconf wg0 /etc/wireguard/wg0.conf
```

### 如何科学上网
接下来就是紧张刺激的正式环节了。
服务端配置：
```shell
$ cat /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.1/24  # 网段
PostUp   = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
ListenPort = 51820
PrivateKey = [SERVER PRIVATE KEY]

[Peer]
PublicKey = [CLIENT PUBLIC KEY]
AllowedIPs = 10.0.0.2/32  # 这表示客户端只有一个 ip。
```
在这之前我们需要开启服务器的ipv4转发：
```shell
$ echo "net.ipv4.ip_forward=1" > /etc/sysctl.conf
$ sysctl -p
解释一下这个，因为我们的网卡是虚拟的wg0，如果我们想要访问外网就需要把发往wg0的请求转发到eth0网卡上，
可以理解为只有这个网卡才能访问外网，而开启linux自带的转发功能是第一步。
```
下面是第二步，就是几条iptables规则：
```shell
$ iptables -A FORWARD -i wg0 -j ACCEPT; 
$ iptables -A FORWARD -o wg0 -j ACCEPT; 
$ iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
开启了数据包转发功能还没有完，我们还需要配置规则，告诉数据包怎么走：
于是我们在FORWARD链配置数据包进出wg0网卡的放行规则，一个进，一个出；
在POSTROUTING链配置SNAT，这里用到了动态SNAT，MASQUERADE，这是为了方便如果有多个公网ip的情况，
正常情况的vps应该只有一个公网ip而且是固定的，那么下面这条规则其实也可以的（速度还快一点😂）：
iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to-source 98.12.141.4
后面的ip就是公网ip，其实就是一个SNAT。

20190718更新：
上面的这一条
$ iptables -A FORWARD -o wg0 -j ACCEPT
其实也可以改成下面这样：
$ iptables -A FORWARD -i eth0 -o wg0 -m state --state ESTABLISHED,RELATED -j ACCEPT
我们用了state模块，让只有已经建立连接的请求才能转发到wg0，这里的连接是对iptables而言的，
不是tcp的连接。对于state模块来说，udp，icmp都是有连接状态的。
这样的话，我们就主动拒绝了从eth0到wg0的请求，可能更安全。
为什么说可能呢，因为我也不知道有没有主动从eth0到wg0的请求会发过来。🤭
```
启动！
```shell
开启
$ wg-quick up wg0
关闭
$ wg-quick down wg0
自启动
$ systemctl enable wg-quick@wg0
```
客户端：
```shell
$ cat /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.2/24  
PrivateKey = [CLIENT PRIVATE KEY]
DNS = 8.8.8.8

[Peer]
PublicKey = [SERVER PUBLICKEY]
AllowedIPs = 0.0.0.0/0, ::0/0   #转发所有流量
Endpoint = [SERVER ENDPOINT]:51820
PersistentKeepalive = 25
```

下面是手机端的配置：
![](/images/photo_2019-09-08_15-36-15.jpg)

注意这个是vpn，就是默认所有流量都转发，访问国内的网站也是走的vpn，所以会比较慢，但是国外的快啊！而且手机端是支持分引应用代理的。😆
而且vpn对于匿名性还是挺不错的，想想别人能知道你访问了什么网站，可怕！

20190730更新：
在一台vps上部署了，但是就是连不上，后来突然发现是selinux的问题
查看SELinux当前状态：
```
$ getenforce
```
临时关闭：
```
$ setenforce 0  
```
或者：
修改/etc/selinux/config 文件
SELINUX=enforcing改为SELINUX=disabled
重启机器即可

引用：    
https://www.wireguard.com/quickstart/
https://wiki.archlinux.org/index.php/WireGuard_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)
