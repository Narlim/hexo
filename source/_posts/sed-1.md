---
title: sed(1)
date: 2019-10-31 20:35:25
tags: linux,tools
---
sed命令总结。所有例子都来自于[http://www.grymoire.com/Unix/Sed.html#uh-13](http://www.grymoire.com/Unix/Sed.html#uh-13)
<!--more-->
### 基本命令s
s for substitution
```shell
sed s/day/night/ old >new

one two three, one two three
four three two one
one hundred
sed 's/one/ONE/' <file
ONE two three, one two three
four three two ONE
ONE hundred

发现第一行只有第一个one被更换，这是s命令的默认行为。

s	  Substitute command
/../../	  Delimiter
one	  Regular Expression Pattern Search Pattern
ONE	  Replacement string
```

### slash作为定界符
```shell
如果匹配的内容包含slash，可以用‘\’转义。
sed 's/\/usr\/local\/bin/\/common\/bin/' <old >new

或者也可以用"_"作为定界符：
sed 's_/usr/local/bin_/common/bin_' <old >new

或者是":":
sed 's:/usr/local/bin:/common/bin:' <old >new

或者是"|":
sed 's|/usr/local/bin|/common/bin|' <old >new
```

### 使用&作为匹配到的字符串
```shell
% echo "123 abc" | sed 's/[0-9]*/& &/'
123 123 abc

正则表达式"[0-9]*"匹配"123"。后面两个"&"表示重复两次。
```

### 扩展正则表达式
```shell
% echo "123 abc" | sed -r 's/[0-9]+/& &/'
123 123 abc
'+'匹配一次或多次
freebsd用'-E'参数。
```

### \1保留模式
```shell
\1是第一个记忆模式，\2是第二个记忆模式。 Sed最多有9种记忆模式。

echo abcd123 | sed 's/\([a-z]*\).*/\1/'
abcd
\1引用前面第一个用'()'匹配的正则。

交换两个匹配的位置：
sed 's/\([a-z]*\) \([a-z]*\)/\2 \1/'
echo '123 abc' | sed 's|\([0-9]*\) \([a-z]*\)|\2 \1|' test
abc 123
或者
sed -r 's/([a-z]+) ([a-z]+)/\2 \1/'

\1也可以用在左边的pattern块中：
消除两个重复的单词：
sed 's|\([a-z]*\) \1|\1|'

打印重复的单词：
sed -n '/\([a-z][a-z]*\) \1/p'

反转前三个字符：
echo 'abc' | sed 's/^\(.\)\(.\)\(.\)/\3\2\1/'
cba
```
