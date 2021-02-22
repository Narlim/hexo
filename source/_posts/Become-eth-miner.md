---
title: 成为一名以太坊矿工
date: 2021-02-22 22:21:35
tags: [miner]
---

看到群里面一个朋友开始挖矿，我也好奇心上来了，也不是想赚什么钱，只要知道显卡挖矿究竟是怎么回事就可以了。

<!--more-->

### 准备
- eth钱包
- 一张好一点的amd或者nvidia的显卡（amd至少rx580，nvidia至少1060吧？如果显卡性能不好的话，收益就低一点，我用的是amd的RX5700xt）
- opencl（amd）或者cuda（nvidia）驱动
- linux系统（或者windows，我这里只说linux系统下的使用）
- 挖矿软件和矿池

**注意：长时间运行挖矿软件会对显卡造成不可逆的损耗，请自行承担风险。（显卡不就是拿来用的吗😝 ）**

### 钱包注册
eth的钱包就是一串独有的地址，交易其实就是一笔对这个地址的转账记录。所以我们只要记住我们的钱包地址就ok了。注册钱包的地方很多，我这里直接的用一个ios的app叫BRD：  
[https://brd.com/](https://brd.com/)
下载然后注册，在eth的收款地址里面会发现一串类似这样的字符：  

0xbc8004340EbEedF12E0da204465a199F1A73bDe4  

这个就是钱包的地址。

当然还有其他的平台很多不同的钱包，都可以用，下面可以参考选择：

[https://bitcoin.org/zh_CN/choose-your-wallet](https://bitcoin.org/zh_CN/choose-your-wallet)

### 显卡
购买一张显卡。

### 驱动
我是下载`archlinux aur`仓库里面的`opencl-amd`这个软件包。
```shell
yay install opencl-amd
```
> 注aur（arch user repository）是由用户主导、用户创建的软件仓库，里面的软件基本都是用户打包发行的。


### 挖矿软件和矿池
挖矿软件也有很多，这里选择的是一个开源的项目叫：ethminer  

[https://github.com/ethereum-mining/ethminer](https://github.com/ethereum-mining/ethminer)  

下载下来，解压，里面有一个二进制文件就是所有了。文档里面也有用法。

矿池我选择：

[https://ethermine.org/](https://ethermine.org/)  

就没什么特殊的理由，看着就很专业🤔

关于矿池的作用具体我也不是很清楚，大概的意思就是你用自己的计算资源通过网络连接到矿池，就可以帮忙挖矿了，当然矿池会把你的奖励返还给你。

好了，万事具备：

```shell
./ethminer -P stratum+ssl://0xbc8004340EbEedF12E0da204465a199F1A73bDe4.WORKERNAME@asia1.ethermine.org:5555
```
将进程放入后台，要不然终端退出，进程也没了，日志也不要了：
```shell
(./ethminer -P stratum+ssl://0xbc8004340EbEedF12E0da204465a199F1A73bDe4.marlin@asia1.ethermine.org:5555 &> /dev/null &)
```

用了ssl加密连接，为了安全。WORKERNAME可以随便填。

呼呼呼。。。显卡终于起飞了。😈

然后你可以在他们官网查看收益，这是我的收益：

[https://ethermine.org/miners/bc8004340EbEedF12E0da204465a199F1A73bDe4/dashboard](https://ethermine.org/miners/bc8004340EbEedF12E0da204465a199F1A73bDe4/dashboard)

他们应该会七天一次将eth的奖励发送到你的钱包。

注：这显卡风扇真的吵，还能不能好好睡觉了。