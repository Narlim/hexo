---
title: bash变量引用
date: 2020-05-05 15:43:18
tags: ['linux', 'bash']
---

关于bash里面的变量引用问题。
<!--more-->

在bash里面，变量引用有两种写法：

```bash
List="one two three"

echo $List
echo "List"
```
一般来说，这两种写法都可以，但是如果原始的字符串里面包含回车，换行等特殊字符的时候就不一样了：

```bash
#!/bin/bash

a='a
b'
echo $a
echo "$a"

# 输出：
a b
a
b
```
可以看到，a后面其实是有一个回车的，只是没有显示出来。用`od`命令可以看到：

```bash
echo $a | od -A d -t c
echo "$a" | od -A d -t c

0000000   a       b  \n
0000004
0000000   a  \n   b  \n
0000004
```
所以说，加双引号的变量引用，保留了原来的格式，而没有加引号的变量引用里面的换行被替换了。
那么是由什么来控制替换的呢？bash的IFS（Internal Field Separator，内部域分隔符）
默认值为空白（包括：空格，tab和新行）。
> Shell 的环境变量分为 set, env 两种，其中 set 变量可以通过 export 工具导入到 env 变量中。其中，set 是显示设置shell变量，仅在本 shell 中有效；env 是显示设置用户环境变量 ，仅在当前会话中有效。换句话说，set 变量里包含了 env 变量，但 set 变量不一定都是 env 变量。这两种变量不同之处在于变量的作用域不同。显然，env 变量的作用域要大些，它可以在 subshell 中使用。

IFS就是一种set变量，当处理命令替换和参数替换时，shell根据IFS的值，默认是space,tab,newline来拆解读入的变量，然后对特殊字符进行处理，最后重新组合赋值给该变量。

所以下面的例子：

```bash
IFS='\'
echo $var        # '(] {}$"
echo "$var"      # '(]\{}$"
```