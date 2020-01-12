---
title: shell基础知识
date: 2020-01-11 22:06:28
tags: ['linux', 'shell']
---

shell基础
<!--more-->

### 管道和重定向

- 重定向
下面的命令演示了STDOUT和STDERR分开处理的原因：

```shell
$ find / -name core
这样会导致很多‘permission denied’这样的信息；
$ find / -name core 2> /dev/null
把错误重定向到/dev/null
$ find / -name core > /tmp/corefiles 2> /dev/null
把匹配的路径重定向到一个文件；
```

- 管道

```shell
$ ps -ef | grep httpd
把httpd进程打印出来；
$ cut -d: -f7 < /etc/passwd | sort -u
把每个用户的shell路径选出来并排序。
```

在一个脚本里，可以用反斜线把一条命令分成多行来写，如果要实现相反的效果，将多条命令整合在一行，可以用分号作为语句分隔符。

### 变量和引用

```shell
$ mylang="Pennsylvania Dutch"
$ echo "I speak ${mylang}"
I speak Pennsylvania Dutch
$ echo 'I speak ${mylang}'
I speak ${mylang}
```

## bash脚本

下面是一个有用的例子：

```shell
$ find . -type f -name '*.log' 2> /dev/null
./leather.log
./foo.log
./genius/spew.log
./.do-not-touch/important.log

需要把‘’.do-not-touch目录排除：
$ find . -type f -name '*.log' 2> /dev/null  | grep -v .do-not-touch  
./leather.log
./foo.log
./genius/spew.log

生成一些新的名字：
$ find . -type f -name '*.log' 2> /dev/null  | grep -v .do-not-touch  | while read fname
> do
> echo mv $fname ${fname/.log/.LOG}
> done
mv ./leather.log ./leather.LOG
mv ./foo.log ./foo.LOG
mv ./genius/spew.log ./genius/spew.LOG

生成的这几条命令就是我们需要的，当我们输入<ctrl-p>的时候，发现bash已经把上面的命令变成了一行：
$ find . -type f -name '*.log' 2> /dev/null | grep -v .do-not-touch  | while read fname; do echo mv $fname ${fname/.log/.LOG}; done | bash -x
加上'bash -x'，执行每条命令之前都会打印这条命令。最后用fc命令把送到用户的默认文本剪辑器，加上必要的#！和说明。
> 修改默认文本编辑器：echo export EDITOR=/usr/bin/vim >> ~/.bashrc
```

总结步骤：

1. 按一个管道的方式开发脚本，完全在命令行上做；

2. 把输出送到标准输出，检查并确保结果正确；

3. 每一步，用<Ctrl-p>重新找回命令；

4. 用fc命令捕获并修改命令；

### 输入和输出

如果要对输出做更多的控制，需要使用printf命令：

```shell
$ printf  "\taa\tbb\tcc"
    aa  bb  cc
```

用read命令可以提示输入：

```shell
#!/bin/bash

echo -n "Enter your name: "
read user_name

if [ -n "$user_name" ]; then
    echo "Hello, $user_name!"
    exit 0
else
    echo "You did not tell you name!"
    exit 1
fi
```

echo命令的-n选项消除了通常的换行符。if的-n判断其字符串参数是否为空。

### 命令行参数与函数

- $1: 第一个参数
- $0: 该脚本所用的名字
- $#: 参数的个数
- $*: 保存有全部的参数

```shell
#!/bin/bash

function show_usage {
    echo "Usage: $0 source_dir dest_dir"
    exit 1
}

# Main program starts here

if [ $# -ne 2 ]; then
    show_usage
else
    if [ -d $1 ]; then
        source_dir=$1
    else
        echo "Invalid source directory"
        show_usage
    fi
    if [ -d $2 ]; then
        dest_dir=$2
    else
        echo "Invalid dest directory"
        show_usage
    fi
fi

printf "Source directory is ${source_dir}\n"
printf "Destination directory is ${dest_dir}\n"
```

可以改进show_usage函数：

```shell
function show_usage {
    echo "Usage: $0 source_dir dest_dir"
    if [ $# -eq 0 ]; then
        exit 99
    else
        exit $1
}

可以给一个确定的出错码值：
show_usage 5
```

在bash里，函数和命令之间很相似，用户可以在自己的~/.bash_profile文件里面定义自己的函数，然后在命令行上使用它们：

```shell
function ssh {
    /usr/bin/ssh -p 7988 $*
}
```

### 变量的作用域

在脚本里的变量是全局变量，但是函数可以用local声明语句，创建自己的局部变量。

### 控制流程

```shell
if [ $base -eq 1 ] && [ $dm -eq 1 ]; then
    installDMBase
elif [ $base -ne 1 ] && [ $dm -eq 1 ]; then
    installBase
elif [ $base -eq 1 ] && [ $dm -ne 1 ]; then
    installDM
else
    echo '==> Install noting'
fi
```
