---
title: 'vim'
date: 2019-06-30 23:11:33
tags: []
published: true
hideInList: false
feature: /post-images/vim.jpg
---
vim快捷键列表及一些基本操作。
<!-- more -->

| 快捷键 | 功能 |
| :------| :------: |
|**移动**| |
| h,j,k,l | 左，下，右，上 | 
| w | 向右移动一个单词（5w，移动5个） |
| b |  向左移动一个单词（同上）|
| ^  | 移动到本行第一个非空字符|
| $ | 移动到本行末尾 | 
| gg | 移到文本开头 |
|  G |  文本末尾 | 
| **插入**|
| i | 光标前插入 |
| a | 光标后插入 |
| A | 本行末尾插入 | 
|  o | 光标下方新起一行插入 | 
| O |  光标上方新起一行插入 | 
|**删除**|
| dd | 删除该行（3dd，删除3行） |
| D | 删除光标至行尾 |
| dw | 删除一个单词 | 
|  d0 | 删除至行首 | 
| dgg |  删除至文件开头 | 
| dG |  删除至文本末尾 | 
| x |  删除光标处字符 |
| X |  删除光标左边单个字符 |
|**修改**|
| r | 替换字符（单个） |
| R | 替换字符（进入替换模式） |
| s | 修改一个字符（直接进入insert模式） | 
|  C | 从光标处删除到行尾，并进入插入模式 | 
| c |  用法同d命令，但是会直接转换为插入模式 | 
| c$ |  替换文本到行尾（直接进入insert模式，功能和“D+i”一样，但是快） | 
| . |  重复前一次操作 |
| u |  撤销前一次操作 |
| Ctrl + r |  还原前一次撤销 |
| yy | 复制一行 |
| 2yy | 复制两行 |
| p | 粘贴 |
|**搜索和替换**|
| /search_text | 搜索 |
| n | 移动到后一个结果 |
| N | 移动到前一个结果 | 
|  :%s/original/replacement/g | 全文替换 | 
| :%s/original/replacement/gc |  全文替换（每次替换前询问） |
| :%s/\<original\>/replacement/g | \<和\>分别为锚定词首和词尾，如果一个单词里面包含original，就不会被匹配到。 | 
|**保存和退出**|
| ZZ | 同:wq |
| ZQ | 同:q! |
| :w new_filename | 用new_filename保存文件 | 
| :! | 执行外部命令（例：:! cat ./another_file） | 
|**翻页**|
| Ctrl + u | 向上翻半页 |
| Ctrl + d | 向下翻半页 |
| Ctrl + b | 向上翻一页 | 
| Ctrl + f | 向下翻一页 | 
|**分屏操作**|
| vim -on file1 file2 | 水平分屏 |
| vim -On file1 file2 | 垂直分屏 |
| Ctrl + w   l | 切换到右边分屏 | 
| Ctrl + w   h | 左边 | 
| Ctrl + w   j | 上边 | 
| Ctrl + w   k | 下边 | 
|**可视化模式**|
| v | 进入单个字符可视模式 |
| V | 进入逐行可视模式 |


-----------------------

### 文本对象及操作
vim的文本对象有w（word）,s（sentence），p(paragraph)和各种引号括号。
范围有i（inner）和a（around）
下面是示例：
`aw`:一个word的around范围。
`iw`：一个word的inner范围，（不包括单词前面或后面的空格）
`i[`或者`i]`:括号内的内容。（其他括号一致）

`ciw`：删除一个word并插入，删除的内容存放在默认寄存器，用命令`:reg ""`可以查看，`""`代表默认无名寄存器。
`daw`：删除一个word及这个单词两边的空格,没有插入。

一般删除用`a`,修改用`i`.
在vim中用`:h text-object`查看文档。


### 列编辑

1. 在normal模式下按ctrl+v进入列编辑模式
2. 通过hjkl选中编辑的区域
3. shift+i 或者 shift+a
4. 输入要插入的内容
5. ctrl+\[或esc

### 块删除：

第一步：按下组合键“CTRL+v” 进入“可视块”模式，选取这一列操作多少行

第二步：按下d 即可删除被选中的整块

### vim宏

普通模式下按qa,开始录制，会把键盘操作录入寄存器，按q结束。@a开始重复命令，10@a重复10次。

### vim插件
#### 安装vundle
这个是一个vim的插件管理器：
```
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
```

#### 修改.vimrc文件
下面是.vimrc文件vundle的配置：
```shell
set nocompatible              " be iMproved, required
filetype off                  " required

" 启用vundle来管理vim插件
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" 安装插件写在这之后

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" 安装插件写在这之前
call vundle#end()            " required
filetype plugin on    " required

" 常用命令
" :PluginList       - 查看已经安装的插件
" :PluginInstall    - 安装插件
" :PluginUpdate     - 更新插件
" :PluginSearch     - 搜索插件，例如 :PluginSearch xml就能搜到xml相关的插件
" :PluginClean      - 删除插件，把安装插件对应行删除，然后执行这个命令即可

" h: vundle         - 获取帮助

" vundle的配置到此结束，下面是你自己的配置
```
我们把插件写上，然后在vim里面执行：
```shell
:PluginInstall
```
等待一下，安装所有插件，可以按`:q`退出界面。

#### git默认编辑器改为vim
nano不太会用= = 
```shell
git config --global core.editor vim
```
或者打开.git/config文件，在core中添加 editor=vim

