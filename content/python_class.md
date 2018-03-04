Title: python 类的一些特点
Date: 2016-01-03
Modified: 2017-04-13 17:32
category: python
tags: __new__, __init__

本篇关于python类的一些特性总结，会持续更新，如果新式类和旧式类表现有差异，会特别说明。未特别说明，才代表新旧式类表现一致。
#### 1：python类__init__方法继承特性    
__init__方法在定义实例的时候会被调用
```python
class test(object);
    def __init__(self, x):
        self.x = x

class test1(test):
    pass

t = test1(10)
print(t.x)
```
执行上面的代码，会打印出10。说明在子类没有显示定义__init__方法时，在定义子类实例时，父类的__init__方法会自动被调用。不过如果子类定义__init__方法，定义子类实例时才不会自动调用父类的__init__方法
```python
class test(object);
    def __init__(self, x):
        self.test_x = x

class test1(test):
    def __init__(self, x):
        self.test1_x = x

t = test1(10)
print(t.test_x)
```
执行上面的代码，会产生如下异常，说明父类的__init__方法在定义实例时（准确的说是定义子类实例）未被调用。
```shell
AttributeError: tesst1 instance has no attribute 'test_x'
```

#### 2：__new__特性及和__init__的区别
`__new__`才是 Python 事实上的构造方法，而 `__init__` 更确切的说是初始化方法。`__new__` 会产生一个实例对象，再把这个实例对象传给`__init__` 绑定一些属性。
因此 `__new__` 是一个类方法，虽然它没有加 classsmethod 装饰器。不过我们大部分时间都不要实现__new__ 方法，因为 Python 解释器会调用 object 对象的 `__new__` 给我们返回一个实例对象。

```python
class test(object):
    def __new__(cls):
        return object.__new__(cls)
```
