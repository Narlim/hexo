---
title: python回调函数
date: 2019-09-10 22:26:46
tags: python
---

了解一下python的回调函数。下面的例子都来自于python3-cookbook。
<!--more-->
### 一个回调函数的示例
先定义一个调用回调函数的函数，可以定义为中间函数：
```python
def apply_async(func, args, *, callback):
    result = func(*args)
    callback(result)
```
下面是回调函数,简单地打印参数：
```python
def print_result(result):
    print('Got:', result)
```
其实这样就可以了，但是这里还有一个add：
```python
def add(x, y):
    return x + y
```

直接调用：
```python
>>> apply_async(add, (2, 3), callback=print_result)
Got: 5
>>> apply_async(add, ('hello', 'world'), callback=print_result)
Got: helloworld
```
其实很简单，就是把一个函数作为参数传递到另一个函数中，那么就可以根据传入不同的函数来“定制”不同的行为，就很灵活。
这里还有一个概念叫“注册回调”，就是把回调函数传入中间函数的动作。还有一个“起始函数”，就是调用中间函数的函数，比如可以是“main”。  
当然回调函数里面还有很多内容，先放一下。

### 扩展
接下来看一下怎么让回调函数访问外部信息。
```python
class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))
```
使用：
```python
>>> r = ResultHandler()
>>> apply_async(add, (2, 3), callback=r.handler)
[1] Got: 5
>>> apply_async(add, ('hello', 'world'), callback=r.handler)
[2] Got: helloworld
```
可以看到前面的数字在增加，说明保存了状态。

还可以用闭包：
```python
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler
```
注意`nonlocal`关键字，表示这个`sequence`是外层函数的变量`sequence`。
使用：
```python
>>> handler = make_handler()
>>> apply_async(add, (2, 3), callback=handler)
[1] Got: 5
>>> apply_async(add, ('hello', 'world'), callback=handler)
[2] Got: helloworld
```

还有一个是使用协程，想就看看：
```python
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
```
需要用`send()`方法作为回调：
```python
>>> handler = make_handler()
>>> next(handler)
>>> apply_async(add, (2, 3), callback=handler.send)
[1] Got: 5
>>> apply_async(add, ('hello', 'world'), callback=handler.send)
[2] Got: helloworld
```

