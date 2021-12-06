---
title: 了解 Linux Network namespace
date: 2021-12-06 09:46:57
tags: ['linux', 'network']
---

network namespace 是一个 linux 对于整个网络栈的一个逻辑上的拷贝，它可以在现有网络栈的基础上创建多个新的独立的网络栈，包含独立的路由，防火墙规则和网络设备。docker 等很多虚拟化技术都使用了 netns 来实现自己的网络功能。

<!--more-->

现在在我的电脑上有两个网卡，正常用有线网卡，然后无线网卡是闲置的，正好可以用它来模拟 netns 的隔离，让一个进程用无线网卡上网。最后这个实验是失败的，因为我本来是想用它来让我的 steam 用无线网卡，从而不走代理（因为我玩游戏的时候连外网有时候会掉线），因为子进程是继承父进程的 netns 的，所以我只要在新的 netns 里面启动 steam 就能实现这样的功能，但是最后发现在新的 netns 下面运行带UI的进程会有问题，但是测试没有UI的进程是可以实现的。所以还是记录一下，说不定哪天服务器上就有这种需求。

### 创建 netns
```bash
# 创建一个名为 steam 的netns
ip netns add steam
ip netns show
steam

# 创建一个 veth pair（veth 类型的网络设备总是成对出现，两头分别接在不同的 netns 就可以实现不同的 netns 之间的通信）
ip link add veth0 type veth peer name veth1
ip link list

# 把 veth1 移动到 steam 这个 netns 下面
ip link set veth1 netns netns1

# 查看 steam netns 下面的网络设备
ip netns exec steam ip link list

1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN mode DEFAULT group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
11: veth1@if12: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether a2:e9:fa:0d:98:9f brd ff:ff:ff:ff:ff:ff link-netnsid 0

# 为veth1分配ip，并启动网卡
ip -n steam addr add 10.0.1.2/24 dev veth1
ip -n steam link set veth1 up
ip -n steam link set lo up
ip -n steam addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
136: veth0@if135: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state LOWERLAYERDOWN group default qlen 1000
    link/ether 26:a7:5a:5f:37:be brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.0.1.2/24 scope global veth0
       valid_lft forever preferred_lft forever

# 创建 bridge 网络设备（其实这里不设置bridge，直接为 veth0 分配ip也是可以的）
ip link add name br0 type bridge
ip addr add 10.0.1.1/24 dev br0
ip link set dev veth0 master br0
ip link set br0 up

# 测试两个 veth 能否互通
ip netns exec steam ping 10.0.1.1
ping 10.0.1.2
```

### 让 netns 能连外网
目前我们只实现了新的 netns 和本机的互通，但是在 steam netns 里面还是不能连百度啥的，因为我们还没有配置路由。
```bash
# 查看 netns 里面的路由,只有一条目标地址为 10.0.1.0/24 网段的路由
ip netns exec steam ip route ls
10.0.1.0/24 dev veth1 proto kernel scope link src 10.0.1.2

# 新建路由，将其他的地址的数据发往 10.0.1.1（也就是veth0）
ip netns exec steam ip route add default via 10.0.1.1 dev veth1

# 做一个 SNAT（MASQUERADE 是一种动态的 SNAT，能自动获取对应网卡的ip地址），让出去的数据包能够回来，wlp6s0 是无线网卡
iptables -t nat -A POSTROUTING -s 10.1.1.0/24 -o wlp6s0 -j MASQUERADE

# 开启ip转发功能
sudo echo 1 > /proc/sys/net/ipv4/ip_forward

# 测试
ip netns exec steam ping 223.5.5.5
```

到这里我们需要明确的一点是，当我们的数据包到达br0这个设备的时候，它查找路由发现了一条默认路由，但是这条默认路由是用的有线网卡，所以它还是从有线网卡出去了，来看一下本机的路由：
```bash
ip route ls
default via 192.168.50.8 dev enp7s0 proto static metric 100
default via 192.168.50.1 dev wlp6s0 proto dhcp metric 600
10.0.1.0/24 dev br0 proto kernel scope link src 10.0.1.2
192.168.2.0/24 dev wg0 proto kernel scope link src 192.168.2.3
192.168.50.0/24 dev enp7s0 proto kernel scope link src 192.168.50.123 metric 100
192.168.50.0/24 dev wlp6s0 proto kernel scope link src 192.168.50.4 metric 600
```
因为我把有线和无线网卡都开启了，配置都正常能上网，所以这里有两条默认路由，但是他们的 metric 值不一样，我们知道 mertic 值越低，优先级越高，所以数据包匹配了第一条路由，经由网卡 enp7s0 出去，这样是不行的。

### 策略路由
既然只能有一条默认路由生效，那我们就需要创建不同的路由表了。

```bash
# 新建路由表 100 并创建路由条目，路由条目就取上面默认表的第二，三，六条
# 这条是系统默认生成的，我们将它移到 table 100
ip route add default via 192.168.50.1 dev wlp6s0 table 100
ip route add 10.0.1.0/24 dev br0 proto kernel scope link src 10.0.1.1  table 100
# 这条也是系统生成的
ip route add 192.168.50.0/24 dev wlp6s0 proto kernel scope link src 192.168.50.4

# 使用 iptable 将标记br0的数据(这里用 raw 表应该也可以，而且 raw 表比 mangle 表更早生效，顺序应该是 raw -> mangle -> nat)
iptables -t mangle -A PREROUTING -i br0 -j MARK --set-mark 100

# 创建 rule，让标记好的数据包使用table 100 来路由
ip rule add fwmark 100 table 100

# 先经过 mangle 表的 PREROUTING 链添加标记，然后再根据策略路由的规则使用 table 100 来路由，这样数据包就能使用无线网卡出去了

# 测试
ip netns exec steam ping 223.5.5.5
```
### 总结
上面的配置都是临时生效，并没有持久化，如果要重启以后还保留配置也可以用 Network Manager 开管理连接。这里的关键是搞清楚数据包的走向，以及相应的规则是在何时生效。总的来说，linux 的网络功能是很灵活的。openwrt 就是一个适用于路由器的 linux 发行版。