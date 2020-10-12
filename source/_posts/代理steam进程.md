---
title: 代理steam进程
date: 2020-10-12 22:02:20
tags: [linux, game]
---

不能访问steam的商店和社区让我很头疼，因为steam不能设置单独的代理，而且我linux环境下用的是shadowsocks-libev,不能支持全局代理什么的。无意中看到cgroup的net_cls可以支持代理进程，只要把steam进程在net_cls里面打上标记就好。

<!--more-->

#### 创建cgroup
```sh
sudo mkdir /sys/fs/cgroup/net_cls/steam

写一个标记到文件中：

cd /sys/fs/cgroup/net_cls/steam
sudo echo 0x00110011 > net_cls.classid

这个整数可以自定义。
```

#### 找到steam的进程

```sh
pgrep steam
```

#### 将进程id写入cgroup.procs
关于进程id写入cgroup.procs还是task,这部分内容涉及到linux的进程和线程的东西，可以看[这里](https://en.wikipedia.org/wiki/Light-weight_process).
```sh
pgrep steam  | awk '{system("echo "$0" | sudo tee /sys/fs/cgroup/net_cls/steam/cgroup.procs")}'
```
我这里用了awk的system函数是因为默认`pgrep`出来的多个结果后面会带一个回车导致不能直接写入`cgroup.procs`文件，用`system`函数就相当于每行都执行一次`echo <pid> | sudo tee`.

#### 加一条iptables规则

还需要把前面cgroup标记的steam流量转发到ss-redir，ss-redir是shadowsocks-libev用来做透明代理的一个组件，具体请看[这里](https://manpages.debian.org/testing/shadowsocks-libev/ss-redir.1.en.html). 这个文档里面还包含了配置一个完整的透明代理的所有步骤。

只要用iptables将出去的流量重定向到ss-redir监听的端口就可以了。(ss-redir的配置和ss-local是一样的。)：

```bash
sudo iptables -t nat -A OUTPUT -p tcp  -m cgroup --cgroup 0x00110011 -j REDIRECT --to-ports 10801
```
--cgroup就是我们前面做的标记。

完成。刷新一下

还有一个问题就是开启steam要手动执行把进程id写入cgroup.procs文件的步骤，因为重启steam进程的id都是会变的，所以还是有点麻烦。关于cgroup和linux进程还有很多的不懂的地方，请大家多多指教！