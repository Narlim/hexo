---
title: python排序总结
date: 2019-09-28 20:49:07
tags: python
---

python序列的排序总结，参考：[https://docs.python.org/zh-cn/3/howto/sorting.html](https://docs.python.org/zh-cn/3/howto/sorting.html)

<!--more-->
#### 基本排序
两个方法，只针对列表的`sort()`方法和针对可迭代对象（list,tuple,dict,set,str等，还有生成器，以及带`yield`的生成器方法）的`sorted()`方法。
`sort()`方法会修改原来的列表，而`sorted()`方法返回一个新的：
```python
>>> a = [5, 2, 3, 1, 4]
>>> sorted(a)
[1, 2, 3, 4, 5]
>>> a
[5, 2, 3, 1, 4]

>>> a.sort()
>>> a
[1, 2, 3, 4, 5]
```
#### 字典排序
```python
from collections import OrderedDict
import json

d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4
for key in d:
    print(key, d[key])

print(json.dumps(d))
```
如果你想要精确控制以 JSON 编码后字段的顺序，可以用`OrderedDict`。
OrderedDict 内部维护着一个根据键插入顺序排序的双向链表。每次当一个新的元素插入进来的时候， 它会被放到链表的尾部。对于一个已经存在的键的重复赋值不会改变键的顺序。

#### 关键函数
`list.sort()`和`sorted()`都有一个key形参来指定在进行比较之前要在每个列表元素上进行调用的函数。
key形参的值应该是一个函数，它接受一个参数并并返回一个用于排序的键。这种技巧速度很快，因为对于每个输入记录只会调用一次key函数。
```python
>>> sorted("This is a test string from Andrew".split(), key=str.lower)
['a', 'Andrew', 'from', 'is', 'string', 'test', 'This']
```
还可以直接用取某个对象的某个值的函数：
```python
>>> student_tuples = [
...     ('john', 'A', 15),
...     ('jane', 'B', 12),
...     ('dave', 'B', 10),
... ]
>>> sorted(student_tuples, key=lambda student: student[2])   # sort by age
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
```
同样的技术也适用于具有命名属性的对象。例如：
```python
>>> class Student:
...     def __init__(self, name, grade, age):
...         self.name = name
...         self.grade = grade
...         self.age = age
...     def __repr__(self):
...         return repr((self.name, self.grade, self.age))
```
```python
>>> student_objects = [
...     Student('john', 'A', 15),
...     Student('jane', 'B', 12),
...     Student('dave', 'B', 10),
... ]
>>> sorted(student_objects, key=lambda student: student.age)   # sort by age
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
```

#### Operator模块
operator 模块有 `itemgetter()` 、 `attrgetter()` 和 `methodcaller()` 函数。
```python
>>> from operator import itemgetter, attrgetter
>>> sorted(student_tuples, key=itemgetter(2))
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

>>> sorted(student_objects, key=attrgetter('age'))
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
```
`attrgetter()`对应的是对象的属性。
还可以多级排序：
```python
>>> sorted(student_tuples, key=itemgetter(1,2))
[('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]

>>> sorted(student_objects, key=attrgetter('grade', 'age'))
[('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]
```
##### 反向
```python
>>> sorted(student_tuples, key=itemgetter(2), reverse=True)
[('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
```

##### 排序稳定性
当多个记录具有相同的键值时，将保留其原始顺序。
```python
>>> data = [('red', 1), ('blue', 1), ('red', 2), ('blue', 2)]
>>> sorted(data, key=itemgetter(0))
[('blue', 1), ('blue', 2), ('red', 1), ('red', 2)]
```
注意 blue 的两个记录如何保留它们的原始顺序，以便 ('blue', 1) 保证在 ('blue', 2) 之前。

##### 排序不支持原生比较的对象
```python
class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return "User({})".format(self.user_id)

def sort_notcompare():
    users = [User(23), User(3), User(99)]
    print(users)
    print(sorted(users, key=lambda u: u.user_id))

或者是用operator模块：
from operator import attrgetter
def sort_notcompare():
    user = [User(23), User(3), User(99)]
    print(users)
    print(sorted(users, key=attrgetter('user_id')))
```
用`attrgetter()`方法会比`lambda`方法快一点。
这个模块也可用于min和max函数：
```python
>>> min(users, key=attrgetter('user_id'))
User(3)
>>> max(users, key=attrgetter('user_id'))
User(99)
```

总结完毕。
