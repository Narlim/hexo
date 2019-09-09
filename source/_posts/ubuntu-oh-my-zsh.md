---
title: 'ubuntu下终端配置：zsh和oh my zsh'
date: 2019-08-10 22:46:37
tags: [shell]
published: true
hideInList: false
feature: /post-images/ubuntu-oh-my-zsh.jpg
---
一直在我的ubuntu机器上用很简陋的terminal，这次配置和美化一下，用起来也舒服一点。在其他的Linux发行版应该也差别不大。
<!-- more -->
### zsh
首先是安装zsh：
zsh是完全兼容bash的，所以bash的脚本zsh都可以跑。
```shell
$ sudo apt install zsh -y
装完以后修改默认的登陆shell：
$ chsh -s /bin/zsh
下次打开terminal就是zsh了环境了，zsh的配置文件在~/.zshrc
```

### [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh)
oh-my-zsh是一个专门配置zsh环境的工具。
直接安装：
```shell
$ sh -c "$(wget -O- https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
它的配置非常多，先不要管它。
```

### 字体
[powerlevel9k](https://github.com/Powerlevel9k/powerlevel9k)是一个powerline类型的主题。它需要安装[Nerd-Fonts](https://github.com/ryanoasis/nerd-fonts)系列字体。
```shell
$ git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/powerlevel9k
编辑~/.zshrc
$ vim ~/.zshrc
添加：
ZSH_THEME="powerlevel9k/powerlevel9k"
source ~/.zshrc

下面是安装字体，推荐用它的脚本自动装，我下载了字体文件安装，terminal里面的配置一直没有，太浪费时间了。
先下载，文件有点大的。。：
$ git clone https://github.com/ryanoasis/nerd-fonts.git
$ ./install.sh Hack
Hack是我选择的字体类型，其他的也可以。
然后在terminal配置里面选择一下字体，我用的是ubuntu自带的。
```
结束以后效果应该是这样：
![](https://narlim.github.io/nototaku/post-images/1565452591706.png)

下面是两个插件
### [ZSH-AUTOSUGGESTIONS](https://github.com/zsh-users/zsh-autosuggestions)
它是一个命令行补全。如果有历史记录里面有相同的命令，它会提示你。
安装它：
```shell
$ git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
下载到了oh-my-zsh的自定义插件目录。
编辑~/.zshrc，添加下面一行：
$ source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
$ source ~/.zshrc
```
查看效果：
![](https://narlim.github.io/nototaku/post-images/1565452606154.png)

紫色的就是提示的，这个颜色是可以修改的：
```shell
$ vim ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=13'
把数字改成其他的就可以了。
```

### [zsh-synax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)
这是一个命令行语法高亮。
```shell
$ git clone https://github.com/zsh-users/zsh-syntax-highlighting.git
$ vim ~/.zshrc
$ source /home/marlin/software/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
$ source ~/.zshrc
```
下面是大概的效果：
![](https://narlim.github.io/nototaku/post-images/1565452618720.png)

20190909更新：  
发现如果目录的路径太长，光标跟着移动，敲命令的空间就会很小。可以修改一些.zshrc文件，在合适的位置添加：  
`POWERLEVEL9K_PROMPT_ON_NEWLINE=true`  
`source ~/.zshrc`  
这样主题的prompt就会显示在光标的上方。光标的开始永远在开头。
