---
title: 'Django的几个字段参数'
date: 2019-07-09 21:59:26
tags: []
published: true
hideInList: false
feature: /post-images/django-de-ji-ge-zi-duan-can-shu.jpg
---
有一些常用的字段参数记录一下。
<!-- more -->

### null
该值为True时，Django在数据库用NULL保存空值。默认值为False。对于保存字符串类型数据的字段，请尽量避免将此参数设为True，那样会导致两种‘没有数据’的情况，一种是NULL，另一种是‘空字符串’。

### blank
True时，字段可以为空。默认False。和null参数不同的是，null是纯数据库层面的，而blank是验证相关的，它与表单验证是否允许输入框内为空有关，与数据库无关。所以要小心一个null为False，blank为True的字段接收到一个空值可能会出bug或异常。

### related_name
反向操作时，使用的字段名，用于代替原反向查询时的'表名_set'。
例如：
```python
class Classes(models.Model):
    name = models.CharField(max_length=32)

class Student(models.Model):
    name = models.CharField(max_length=32)
    theclass = models.ForeignKey(to="Classes")
```
当我们要查询某个班级关联的所有学生（反向查询）时，我们会这么写：
```python
models.Classes.objects.first().student_set.all()
```
当我们在ForeignKey字段中添加了参数 related_name 后，
```python
class Student(models.Model):
    name = models.CharField(max_length=32)
    theclass = models.ForeignKey(to="Classes", related_name="students")
```
当我们要查询某个班级关联的所有学生（反向查询）时，我们会这么写：
```python
models.Classes.objects.first().students.all()
```

### on_delete
这个表示外键被删除的时候，所关联的对象应该进行什么操作。比如说一篇文章对应一个Python的分类，但是这个分类被你不小心删除了，那么这篇文章的分类应该会发生什么变化呢？主要有以下六种：
1. CASCADE：模拟SQL语言中的ON DELETE CASCADE约束，将定义有外键的模型对象同时删除！（该操作为当前Django版本的默认操作！）
2. PROTECT：阻止上面的删除操作，但是弹出ProtectedError异常
3. SET_NULL：将外键字段设为null，只有当字段设置了null=True时，方可使用该值。
4. SET_DEFAULT：将外键字段设为默认值。只有当字段设置了default参数时，方可使用。
5. DO_NOTHING：什么也不做。
6. SET()：设置为一个传递给SET()的值或者一个回调函数的返回值。注意大小写。

下面两个是时间字段独有的。
### auto_now_add
配置auto_now_add=True，创建数据记录的时候会把当前时间添加到数据库。
### auto_now
配置上auto_now=True，每次更新数据记录的时候会更新该字段。
