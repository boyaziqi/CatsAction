Title: python类特殊方法
Date: 2017-06-06 22:42:00
category: python
tags: __call__

#### __init_\_
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
执行上面的代码，会打印出10。说明在子类没有显示定义__init__方法时，在定义子类实例时，父类的__init__方法会自动被调用。
不过如果子类定义__init__方法，定义子类实例时不会自动调用父类的__init__方法
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

#### \__new__
`__new__`才是 Python 事实上的构造方法，而 `__init__` 更确切的说是初始化方法。`__new__` 会产生一个实例对象，再把这个实例对象传给`__init__` 绑定一些属性。
因此 `__new__` 是一个类方法，虽然它没有加 classsmethod 装饰器。不过我们大部分时间都不要实现__new__ 方法，因为 Python 解释器会调用 object 对象的 `__new__` 给我们返回一个实例对象。

```python
class test(object):
    def __new__(cls, *args, **kwargs):
        return super(test, cls).__new__(cls, *args, **kwargs)
```

#### \_\_call\_\_
当一个类实现了__call__方法时，它的实例就是可调用的。即像函数一样使用。
```python
class CallTest(object):
    def __init__(self, name):
        print(name)

    def __call__(self, x, y):
        print("sum:", x+y)
``` 
```shell
t = CallTest("test")
t(1,2)
```

上面将会输出:
```shell
test
sum: 3
```
从输出结果我们可以看到，__init__在创建实例的时候被调用，用来初始化一些属性。而__call__在实例被像函数一样调用时被调用。

> python3中，类是type的实例，用dir(type)查看type的方法时，可以看见type实现了__call__方法，因此在定义类的时候会调用对应的__call__方法，这也是
> 元类的工作方式。关于元类，可以查看我的其他文章。同样，函数也实现了__call__方法

#### \_\_getitem__ \_\_getattribute__ \_\_getattr__
这里把三个属性放在一起讨论，方便区别

- \_\_getitem__ 在a['a'] 时被调用
- \_\_getattr__ 在某个实例属性不存在的时候被调用
- \_\_getattribute__ 是无条件被调用.对任何对象的属性访问时,都会隐式的调用__getattribute__方法
