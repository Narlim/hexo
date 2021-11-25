---
title: DNS分流
date: 2021-06-23 20:55:08
tags: ['linux', 'dns']
---

记录一下最近几天在搞的一个更舒服地上网的方案，尽量讲得详细一点。
参考的文章是：[博客](https://jeremyxu2010.github.io/2020/02/%E4%BA%AB%E5%8F%97%E8%87%AA%E7%94%B1%E7%9A%84%E7%BD%91%E7%BB%9C/)
有几个点和这篇文章不太一样，都会详细写出。

<!--more-->

用到的几个开源项目：
- [shadowsocks-libev](https://github.com/shadowsocks/shadowsocks-libev)
- [privoxy](http://www.privoxy.org/): http代理
- [dnsmasq](): dns服务器
- [dnscrypt-proxy](https://github.com/DNSCrypt/dnscrypt-proxy): 加密dns请求代理
- [dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list): 国内域名列表。

### shadowsocks-libev
服务器配置：
```json
{
    "server":["0.0.0.0"],
    "mode":"tcp_and_udp",
    "server_port":18388,
    "password":"<PASSWORD>",
    "timeout":60,
    "method":"chacha20-ietf-poly1305",
    "nameserver": "208.67.222.222",
    "fast_open": true,
    "no_delay": true
}
```
这里我开启了`no_delay`这个参数，表示关闭tcp的Nagle算法，这个算法大概的意思就是tcp发包的时候，如果发送的数据量没有达到一定的值，会等一下后面的数据再发，这样无疑增加了网络的延迟;而关闭的意思就是如果有了哪怕一点数据就发送，不用等待。感兴趣的话可以去了解一下。这个参数具体对于网速究竟有没有提升不是很清楚，反正我开了。

#### 服务器的内核参数优化


### privoxy
这个软件是一个比较老的http代理软件，老不代表差，主要就是用它来做分流。  
上面那篇文章里面用的是GFW黑名单，意思就是维护一个全部被墙的域名列表，如果请求的域名在列表里面就走代理，如果不在就直连，这样有一个弊端就是如果有新的网站被墙，而列表没有及时更新的话，访问就还是困难。所以我这里就选择另一个方案，白名单;如果访问的域名不在列表里面，全部走代理。

但是我好像没有找到适合`privoxy`的白名单这样的配置，国内域名的列表是有，就是这个：[https://github.com/felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list)，那就用这个列表来自己动手生成一个配置文件。

因为后面也是要用到`dnsmasq`，也需要这个配置，所以先安装`dnsmasq`并配置。

### dnsmasq
dnsmasq我们用它的dns分流和dns缓存功能。

```shell
sudo pacman -S dnsmasq

wget https://github.com/felixonmars/dnsmasq-china-list

# 修改一下dns
sudo ./install.sh
```
会发现`/etc/dnsmasq.d`下面多了一些文件，
```shell
-rw-r--r-- 1 root root 2.0M Jun  8 20:37 accelerated-domains.china.223.5.5.5.conf
-rw-r--r-- 1 root root 2.0M Jun  8 20:37 accelerated-domains.china.223.6.6.6.conf
-rw-r--r-- 1 root root 5.2K Jun  8 20:37 apple.china.223.5.5.5.conf
-rw-r--r-- 1 root root 5.2K Jun  8 20:37 apple.china.223.6.6.6.conf
-rw-r--r-- 1 root root 5.3K Jun  8 20:37 bogus-nxdomain.china.conf
-rw-r--r-- 1 root root 1.9K Jun  8 20:37 google.china.223.5.5.5.conf
-rw-r--r-- 1 root root 1.9K Jun  8 20:37 google.china.223.6.6.6.conf
```
后面还会用到。
再来修改一下`dnsmasq`本身的配置，在`/etc/dnsmasq.conf`：
```shell
no-resolv

# 将请求转发到5300端口的上游dns服务器，后面会提到。

server=127.0.0.1#5300

# 默认监听在127.0.0.1的53端口

listen-address=127.0.0.1

# 该目录下在域名dns请求都走配置的国内dns服务器，这里就是上面的233.5.5.5和233.6.6.6

conf-dir=/etc/dnsmasq.d
```
重启`dnsmasq`.

### privoxy
接下来继续来配置没配置完的`privoxy`白名单：
```shell
因为privoxy的配置是以'.action'结尾的：

cut -f 2 -d/ accelerated-domains.china.223.6.6.6.conf | sudo tee direct.action
cut -f 2 -d/ apple.china.223.6.6.6.conf | sudo tee -a direct.action
cut -f 2 -d/ google.china.223.6.6.6.conf | sudo tee -a direct.action

然后编辑'direct.action'，在所有的域名前面加上"."，并且在第一行加上"{+forward-override{forward .}}"，表示下面这些请求直连。
```
将`direct.action`文件移动到目录`/etc/privoxy`。

然后编辑主配置文件`config`：
```shell
找到'actionsfile'
...
actionsfile match-all.action
actionsfile default.action   
actionsfile user.action      
actionsfile direct.action # 关键是在这里加上这个
...

listen-address  127.0.0.1:8118

...
# 这个是本地的socks5代理客户端监听的端口，这里的意思是将所有的请求发送到本地代理客户端。
因为前面的actionsfile将所有直连的请求过滤了，所以后面的所有请求走代理。

forward-socks5t   /         127.0.0.1:1080 .  
```
重启`privoxy`.

### dnscrypt-proxy
这个软件是加密dns请求，其实http代理本身会解析dns请求，而且由于我们是socks5代理，dns请求会被发送到远端服务器解析，也就是前面在ss里面配置的'nameserver'，这样也有一个好处就是保证socks5代理服务器获得的dns解析的ip是有cdn优化的，比如新加坡的代理解析出来的就是新加坡的服务器。这样我们只要保证我们的域名白名单没问题，就不会发生国内的域名解析到国外的ip。  
但是还有一些本地的应用也需要走代理，但是它不读取系统的http代理配置，那么就会用本地的dns解析，从而可能获得污染的dns结果，所以还是要在`dnsmasq`分流一下，部署`dnscrypt-proxy`, 编辑`dnscrypt-proxy.toml`:
```toml
比较重要的几个配置：

server_names = ['google']

listen_addresses = ['127.0.0.1:5300']

ipv6_servers = false

# 因为我们的ss开启了udp转发，所有这里不用tcp

force_tcp = false

# dns代理其实还是走了socks5代理，所以应该是dns over socks5?

proxy = 'socks5://127.0.0.1:1080'

fallback_resolvers = ['9.9.9.9:53', '8.8.8.8:53']

cache ture
```
重启，从日志中可以看到，它使用了'DoH'(dns over https)。

### 本机及浏览器配置
打开电脑的网络设置，添加http代理：HTTP_PROXY:127.0.0.1:8118,HTTPS_POROXY:127.0.0.1:8118   

浏览器打开设置，同样设置http代理。

完成！

### dns泄漏
其实用http代理的还有一个原因就是如果你直接用浏览器设置socks5代理，会有dns泄漏的风险，就是说虽然socks5是远程dns解析，但是浏览器在解析dns的时候可能还是用的本地的dns解析。isp还是能够看到你要访问的网站是什么。[http://www.chromium.org/developers/design-documents/network-stack/socks-proxy](http://www.chromium.org/developers/design-documents/network-stack/socks-proxy)
所以这也是一个要在本地搭建一个加密dns服务器的原因之一。
也有很多网站可以测试dns泄漏问题。就是如果你配置了代理，但是你的dns服务器还是用的isp的，而不是代理的，那么就是dns泄漏。很多vpn如果配置不正确也会有dns泄漏问题。**你以为你在匿名访问一些网站其实被isp看得一清二楚。**

### 总结
上面一些开源软件的功能都异常强大，这里只用了很小一部分的功能。如果有错误的地方请大家指出，其实还有更好的方案就是用v2ray,v2ray一个软件应该就能做上面的所有事情。但是我不太会配置v2ray,所有用了上面的方案。最关键的是上面的白名单，感觉确实比黑名单要好很多，也解决了dns污染和dns泄漏问题。