---
title: 'yum包管理器'
date: 2019-06-29 16:29:53
tags: [linux]
published: true
hideInList: false
feature: /post-images/yum-bao-guan-li-qi.jpg
---
yum和rpm

<!-- more -->
[维基百科](https://zh.wikipedia.org/wiki/Yellowdog_Updater,_Modified)

最常用的几个命令：
* install：安装
* update：更新
* remove：删除
* search：搜索
* localinstall：安装本地rpm包


下面演示一下安装nginx：
### 搜索
```
# yum search nginx

collectd-nginx.x86_64 : Nginx plugin for collectd
munin-nginx.noarch : NGINX support for Munin resource monitoring
nextcloud-nginx.noarch : Nginx integration for NextCloud
nginx-all-modules.noarch : A meta package that installs all available Nginx modules
nginx-filesystem.noarch : The basic directory layout for the Nginx server
nginx-mod-http-geoip.x86_64 : Nginx HTTP geoip module
nginx-mod-http-image-filter.x86_64 : Nginx HTTP image filter module
nginx-mod-http-perl.x86_64 : Nginx HTTP perl module
nginx-mod-http-xslt-filter.x86_64 : Nginx XSLT module
nginx-mod-mail.x86_64 : Nginx mail modules
nginx-mod-stream.x86_64 : Nginx stream modules
owncloud-nginx.noarch : Nginx integration for ownCloud
pcp-pmda-nginx.x86_64 : Performance Co-Pilot (PCP) metrics for the Nginx Webserver
python2-certbot-nginx.noarch : The nginx plugin for certbot
nginx.x86_64 : A high performance web server and reverse proxy server

  Name and summary matches only, use "search all" for everything.
```
搜出来好多，仔细看一下最后一个才是，但是上面也没有显示nginx的版本，如果我们要安装具体的某一个版本怎么办？

先查看源里面nginx的版本：
```
# yum info nginx.x86_64

Available Packages
Name        : nginx
Arch        : x86_64
Epoch       : 1
Version     : 1.12.2
Release     : 3.el7
Size        : 531 k
Repo        : epel/x86_64
Summary     : A high performance web server and reverse proxy server
URL         : http://nginx.org/
License     : BSD
Description : Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and
            : IMAP protocols, with a strong focus on high concurrency, performance and low
            : memory usage.
```
如果要安装其他版本的，就需要添加源了：
```
vim /etc/yum.repos.d/nginx.repo
```

### 删除
```
yum remove nginx
yum erase nginx
```

### 查看某个名字在哪个包里面
```
yum provides nginx
```

### yum配置http代理
```
在/etc/yum.conf后面添加以下内容：
proxy=http://代理服务器IP地址:端口号

如果需要认证:
proxy=http://代理服务器IP地址:端口号
proxy_username=代理服务器用户名
proxy_password=代理服务器密码
```



