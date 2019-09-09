---
title: 'lsof命令'
date: 2019-08-23 23:56:56
tags: []
published: true
hideInList: false
feature: /post-images/lsof-ming-ling.jpg
---
lsof（list open files）是一个查看当前系统文件的工具。
mac下面可以用来查看端口的进程，因为mac的netstat命令有点鸡肋。当然它是linux一个挺强大的命令。
<!-- more -->

#### 查看打开某个文件的进程：
```shell
$ sudo lsof /var/log/message
```


#### 查看一个目录下所有被打开的文件：
```shell
[root@host ~]# lsof +D /var/log/
COMMAND    PID  USER   FD   TYPE DEVICE SIZE/OFF   NODE NAME
auditd     584  root    4w   REG    8,2  2732150     97 /var/log/audit/audit.log
rsyslogd  1125  root    5w   REG    8,2   266813  18147 /var/log/messages
rsyslogd  1125  root    6w   REG    8,2    87325   6283 /var/log/cron
rsyslogd  1125  root    7w   REG    8,2     2254  31941 /var/log/secure
tuned    10484  root    3w   REG    8,2    17357    159 /var/log/tuned/tuned.log
nginx    11542  root    2w   REG    8,2        0 262694 /var/log/nginx/error.log
```

#### 查看被某个进程打开的所有文件：
```shell
[root@host ~]# lsof -c bash
COMMAND   PID USER   FD   TYPE DEVICE  SIZE/OFF  NODE NAME
bash    10434 root  cwd    DIR    8,2      4096    22 /root
bash    10434 root  rtd    DIR    8,2      4096     2 /
bash    10434 root  txt    REG    8,2    964608  4482 /usr/bin/bash
bash    10434 root  mem    REG    8,2     61624 32056 /usr/lib64/libnss_files-2.17.so
bash    10434 root  mem    REG    8,2 106075056 14953 /usr/lib/locale/locale-archive
bash    10434 root  mem    REG    8,2   2151672  4112 /usr/lib64/libc-2.17.so
bash    10434 root  mem    REG    8,2     19288 32052 /usr/lib64/libdl-2.17.so
```

#### 查看被一个用户打开的所有文件：
```shell
[root@host ~]# lsof -u nginx
COMMAND   PID  USER   FD      TYPE             DEVICE SIZE/OFF    NODE NAME
nginx   11543 nginx  cwd       DIR                8,2     4096       2 /
nginx   11543 nginx  rtd       DIR                8,2     4096       2 /
nginx   11543 nginx  txt       REG                8,2  1333536   31927 /usr/sbin/nginx
nginx   11543 nginx  mem       REG                8,2    61624   32056 /usr/lib64/libnss_files-2.17.so
nginx   11543 nginx  mem       REG                8,2   155784     258 /usr/lib64/libselinux.so.1
nginx   11543 nginx  mem       REG                8,2   105824   32058 /usr/lib64/libresolv-2.17.so
```

#### 查看某个进程打开的文件：
```shell
$ lsof -p 1135
```

#### 查看某个打开某个文件的进程id：
```shell
[root@host ~]# lsof -t /var/log/messages
1125
```

#### 查看所有网络相关的文件：
```shell
[root@host ~]# lsof -i
COMMAND     PID   USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
chronyd     655 chrony    1u  IPv4   15322      0t0  UDP localhost:323
chronyd     655 chrony    2u  IPv6   15323      0t0  UDP localhost:323
dhclient    755   root    6u  IPv4   16024      0t0  UDP *:bootpc
v2ray      1118   root    3u  IPv6 1169149      0t0  UDP *:18298
v2ray      1118   root    5u  IPv6 1169150      0t0  UDP *:16137
sshd       1122   root    3u  IPv4   17803      0t0  TCP *:28369 (LISTEN)
sshd       1122   root    4u  IPv6   17806      0t0  TCP *:28369 (LISTEN)
ss-server  1132 nobody    5u  IPv4   17565      0t0  TCP *:ddi-tcp-1 (LISTEN)
ss-server  1132 nobody    6u  IPv4   17567      0t0  UDP *:ddi-udp-1
master     1572   root   13u  IPv4   19251      0t0  TCP localhost:smtp (LISTEN)
master     1572   root   14u  IPv6   19252      0t0  TCP localhost:smtp (LISTEN)
sshd      10616   root    3u  IPv4 1169210      0t0  TCP 98.142.141.74.16clouds.com:28369->58.101.120.88:62368 (ESTABLISHED)
```


#### 查看某个进程id打开的网络文件：
```shell
[root@host ~]# sudo lsof -i -a -p 11542
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nginx   11542 root    6u  IPv4  17747      0t0  TCP *:http (LISTEN)
nginx   11542 root    7u  IPv4  17750      0t0  TCP *:mysql (LISTEN)
```

#### 查看某个命令的网络连接打开的文件：
```shell
[root@host ~]# sudo lsof -i -a -c ssh
COMMAND   PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
sshd     1122 root    3u  IPv4   17803      0t0  TCP *:28369 (LISTEN)
sshd     1122 root    4u  IPv6   17806      0t0  TCP *:28369 (LISTEN)
sshd    10616 root    3u  IPv4 1169210      0t0  TCP 98.142.141.74.16clouds.com:28369->58.101.120.88:62368 (ESTABLISHED)
```

#### 查看某个端口打开的文件：
```shell
[root@host ~]# lsof -i :28369
COMMAND   PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
sshd     1122 root    3u  IPv4   17803      0t0  TCP *:28369 (LISTEN)
sshd     1122 root    4u  IPv6   17806      0t0  TCP *:28369 (LISTEN)
sshd    10616 root    3u  IPv4 1169210      0t0  TCP 98.142.141.74.16clouds.com:28369->58.101.120.88:62368 (ESTABLISHED)
```

#### 查看某个网络协议打开的文件：
```shell
[root@host ~]# sudo lsof -i tcp
COMMAND     PID   USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
sshd       1122   root    3u  IPv4   17803      0t0  TCP *:28369 (LISTEN)
sshd       1122   root    4u  IPv6   17806      0t0  TCP *:28369 (LISTEN)
ss-server  1132 nobody    5u  IPv4   17565      0t0  TCP *:ddi-tcp-1 (LISTEN)
master     1572   root   13u  IPv4   19251      0t0  TCP localhost:smtp (LISTEN)
master     1572   root   14u  IPv6   19252      0t0  TCP localhost:smtp (LISTEN)
sshd      10616   root    3u  IPv4 1169210      0t0  TCP 98.142.141.74.16clouds.com:28369->58.101.120.88:62368 (ESTABLISHED)
nginx     11542   root    6u  IPv4   17747      0t0  TCP *:http (LISTEN)
```
--------
最后是一些参数：
- -a 列出打开文件存在的进程
- -c<进程名> 列出指定进程所打开的文件
- -g  列出GID号进程详情
- -d<文件号> 列出占用该文件号的进程
- +d<目录>  列出目录下被打开的文件
- +D<目录>  递归列出目录下被打开的文件
- -i<条件>  列出符合条件的进程。（4、6、协议、:端口、 @ip ）
- -p<进程号> 列出指定进程号所打开的文件
- -u  列出UID号进程详情
