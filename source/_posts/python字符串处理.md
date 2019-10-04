---
title: python字符串处理
date: 2019-10-01 21:54:21
tags: python
---

### 使用多个界定符分隔字符串
```python
import re
line = 'asdf fjdk; afed, fjek,asdf, foo'
result = re.split(r'[,;\s]\s*', line)
print(result)
```
使用re模块，使用正则匹配',',';'以及空格，并且在分隔符后面可以带多个空格。

### 字符串开头或结尾匹配
```python
>>> filename = 'spam.txt'
>>> filename.endswith('.txt')
True
>>> filename.startswith('file:')
False
>>> url = 'http://www.python.org'
>>> url.startswith('http:')
True
```
如果你想检查多种匹配可能，只需要将所有的匹配项放入到一个元组中去， 然后传给 startswith() 或者 endswith() 方法：
```python
>>> import os
>>> filenames = os.listdir('.')
>>> filenames
[ 'Makefile', 'foo.c', 'bar.py', 'spam.c', 'spam.h' ]
>>> [name for name in filenames if name.endswith(('.c', '.h'))]
['foo.c', 'spam.c', 'spam.h'
>>> any(name.endswith('.py') for name in filenames)
True
```
下面是另一个例子：
```python
from urllib.request import urlopen

def read_data(name):
    if name.startswith(('http:', 'https:', 'ftp:')):
        return urlopen(name).read()
    else:
        with open(name) as f:
            return f.read()
```
如果传入的是三个协议的url，用urlopen方法读取数据，否则直接作为文件数据读取。
检查某个文件夹中是否存在指定的文件类型：
```python
if any(name.endswith('.c', '.h') for name in listdir(dirname)):
...
```