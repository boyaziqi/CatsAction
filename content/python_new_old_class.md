Title: python 新式类和旧式类的一些理解
Date: 2017-10-18 10:37:00
category: python

> 下面是两个类,一个新式类，一个旧式类

```python
class OldClass():
    pass

class NewClass(object):
    pass

old_instance = OldClass()
new_instance = NewClass()
```

> 下面是我在ipython运行测试的结果

```python
In [15]: class OldClass():
    ...:     pass
    ...:
In [16]: class NewClass():
    ...:     pass
    ...:
In [17]: old_instance = OldClass()

In [18]: new_instance = NewClass()
In [19]: type(old_instance)
Out[19]: instance
In [23]: type(new_instance)
Out[23]: __main__.NewClass
In [24]: print(type(old_instance))
<type 'instance'>

In [25]: print(type(new_instance))
<class '__main__.NewClass'>
In [26]: type(1)
Out[26]: int
In [27]: print(type(1))
<type 'int'>
In [31]: type(1) == int
Out[31]: True
In [32]: type(1) is int
Out[32]: True
In [33]: type(old_instance) is OldClass
Out[33]: False
In [34]: type(new_instance) is NewClass
Out[34]: True
```

* 通过上面，我们看到，旧式类，一切实例的类型均是`instance`。它和内置类型表现形式不一致，这样不能很好的体现实例和类之间的关系。
而新式类则使类和内置类型表现形式一致。为了判断一个实例是否属于一个类，旧式类最可靠的方式时`instance()`内置方法，新式类可以
通过`type`判断，和内置类型一致。

> 下面是类本身的特性
```python
In [37]: print(type(1))
<type 'int'>
In [38]: print(type(OldClass))
<type 'classobj'>
In [39]: print(type(NewClass))
<type 'type'>

In [40]: print(type(int))
<type 'type'>
```
* 新式类的的类型是`type`，这和内置类型一致。旧式类则不是
--------------------
 *注:最新的python版本将内置类型也统一成类的形式，`print(type(int)`将打印`<class 'type'>`。以后我觉得更精准的称呼应该是内置类和
 自定义类*
