---
title: VS Code字体推荐：Fira Code
date: 2019-09-08 09:55:11
tags: [tips, vscode]
---

在别人的推荐下用了这个字体，发现真的很不错，看起来很舒服，也比较适合写代码。
### 项目地址
[github地址](https://github.com/tonsky/FiraCode)  
可以在里面看到具体的效果。

### 设置步骤
#### 下载安装
到[这里](https://github.com/tonsky/FiraCode/tree/master/distr/ttf)下载需要的字体，鼠标双击打开就可以安装了。  
上面的方法安装字体还是挺通用的，不过如果你不想用鼠标双击并且用的恰好是ubuntu的话：
##### 开启universe repository
```shell
$ sudo add-apt-repository universe
```
##### 安装firacode字体
```shell
$ sudo apt install fonts-firacode
```
当然你如果是其他发行版的话都有对应的安装方法的。[wiki](https://github.com/tonsky/FiraCode/wiki)

#### 设置vscode
直接快捷键`ctrl+,`打开设置文件，修改fontfamily为`Fira Code`