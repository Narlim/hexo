---
title: 'centos7更新内核'
date: 2019-07-28 15:10:16
tags: []
published: true
hideInList: false
feature: /post-images/centos7-geng-xin-nei-he.jpg
---
更新内核以支持wireguard，如果上一篇文章安装wireguard有问题，可以看这个步骤更新内核，😂
<!-- more -->
### centos 7 更新内核
```shell
添加ELRepo：
$ sudo yum -y install https://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm

导入GPG key
$ sudo rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org

查看：
$ sudo yum --disablerepo="*" --enablerepo="elrepo-kernel" list available | grep kernel-ml

安装：
$ sudo yum --enablerepo=elrepo-kernel install kernel-ml

顺便装上这些东西（这个是wireguard必须的，而且如果你安装wireguard的时候装的版本可能和你的内核版本对不上）：
$ sudo yum -y --enablerepo=elrepo-kernel install kernel-ml-{devel,headers,perf}

修改grub，并保存：
Edit the file /etc/default/grub and set GRUB_DEFAULT=0
$ sudo grub2-mkconfig -o /boot/grub2/grub.cfg

重启。

删除更新的内核：
$ uname -r
3.10.0-957.1.3.el7.x86_64
确认自己在3.10

删除
$ sudo yum remove kernel-ml kernel-ml-{devel,headers,perf}
```
