---
title: shell基础知识
date: 2020-01-11 22:06:28
tags: ['linux', 'shell']
---


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

