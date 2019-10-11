---
title: python函数
date: 2019-10-10 21:21:36
tags: python
---
python函数总结, 流畅的python.
<!--more-->

### 函数作为对象
下面的示例展示了函数作为一等对象的本性：
```python
def factorial(n):
    return 1 if n < 2 else n * factorial(n-1)

fact = factorial
fact(5)
120
map(factorial, range(11))
list(map(fact, range11))
[1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]

可以把函数作为参数传递给map函数。
```
下面是“一等对象”的定义：
- 在运行时创建
- 能赋值给变量或数据结构中的元素
- 能作为参数传给函数
- 能作为函数的返回结果
有了一等函数就可以使用函数式编程风格，特点之一就是使用高阶函数。

### 高阶函数
接受函数为参数,或者把函数作为结果返回的函数是高阶函数。map函数就是，还有内置的sorted函数，可选的key参数用于提供一个函数。
```python
>>> fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
>>> sorted(fruits, key=len)
['fig', 'apple', 'cherry', 'banana', 'raspberry', 'strawberry']
```
根据反向拼写给单词一个排序：
```python
def reverse(word):
    return word[::-1]
>>> reverse('testing')
'gnitset'
>>> sorted(fruits, key=reverse)
['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']
```
#### map、filter和reduce的现代替代品
map 和 filter 与列表推导比较:
```python
>>> list(map(fact, range(6)))
[1, 1, 2, 6, 24, 120]
[fact(n) for n in range(6)]
[1, 1, 2, 6, 24, 120]
>>> list(map(factorial, filter(lambda n: n % 2, range(6))))
[1, 6, 120]
>>> [factorial(n) for n in range(6) if n % 2]
[1, 6, 120]
```
使用 reduce 和 sum 计算 0~99 之和:
```python
>>> from functools import reduce
>>> from operator import add
>>> reduce(add, range(100))
4950
>>> sum(range(100))
4950
```
为了使用高阶函数,有时创建一次性的小型函数更便利。这便是匿名函
数存在的原因.

#### 匿名函数

lambda关键字在python表达式内创建匿名函数。
```python
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
sorted(fruits, key=lambda word: word[::-1])
```
和def语句一样，lambda表达式会创建函数对象，这是python中几种可调用对象的一种。

