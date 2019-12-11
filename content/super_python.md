Title: Python super 函数的理解
Date: 2016-03-10 21:12
category: python
tags: super

### super 是一个类

当我们调用 super() 的时候，实际上是实例化了一个 super 类。你没看错， super 是个类，既不是关键字也不是函数等其他数据结构:

```python
In [1]: class Test(object):
   ...:     pass
   ...:
In [2]: s = super(Test)
In [3]: type(s)
Out[3]: super
```

在大多数情况下， super 包含了两个非常重要的信息: 一个 MRO 以及 MRO 中的一个类。当以如下方式调用 super 时:

```python
super(a_type, obj)
```

MRO 指的是 type(obj) 的 MRO, MRO 中的那个类就是 a_type , 同时 isinstance(obj, a_type) == True 。

当这样调用时:

```python
super(type1, type2)
```

MRO 指的是 type2 的 MRO, MRO 中的那个类就是 type1 ，同时 issubclass(type2, type1) == True 。

### super 具体怎么工作

如上面所说，super 包含一个 MRO 和 MRO 中的一个类，假如 MRO 如下：

```python
[A, B, C, D, E, object]
```

那么 `super(C, A).method()` 将从 D，E，object 中查找 method 方法。并将 method 方法调用时的 self 设置为 A。

如下的多继承例子：

```python
class A:
    def __init__(self):
        self.n = 2

    def add(self, m):
        print('self is {0} @A.add'.format(self))
        self.n += m


class B(A):
    def __init__(self):
        self.n = 3

    def add(self, m):
        print('self is {0} @B.add'.format(self))
        super().add(m)
        self.n += 3


class C(A):
    def __init__(self):
        self.n = 4

    def add(self, m):
        print('self is {0} @C.add'.format(self))
        super().add(m)   # 相当于 super(D, self).add(m)
        self.n += 4


class D(B, C):
    def __init__(self):
        self.n = 5

    def add(self, m):
        print('self is {0} @D.add'.format(self))
        super(C, D).add(self, m)  # super 第二个参数为类对象时，需要显示传递self
        self.n += 5

if __name__ == '__main__':
    d1 = D()
    d2 = D()
    d1.add1(2)
    print(d1.n, '=================')
    d2.add2(2)
    print(d2.n, '=================')

    print(D.__mro__)   # D 的 MRO
```

输出结果如下：
```bash
self is <__main__.D object at 0x10e15e320> @D.add1
self is <__main__.D object at 0x10e15e320> @B.add
self is <__main__.D object at 0x10e15e320> @C.add
self is <__main__.D object at 0x10e15e320> @A.add
19 =================
self is <__main__.D object at 0x10e15e6a0> @D.add2
self is <__main__.D object at 0x10e15e6a0> @A.add
12 =================
(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>,
<class '__main__.A'>, <class 'object'>)
```

说明：

> - 从输出结果可以看到，super 可以避免重复调用一个方法的问题。
> - super().add(m) 等于 super(D, self).add(m)，前者是后者的简写形式。
> - 当 super() 的第二个参数是一个类对象时，需要显示的将实例对象传递给父类的方法。这也是 add1 和 add2 的主要区别。
>这其实很好理解，因为第二个参数为类对象时，super 返回的是一个非绑定方法，因此需要显示的指定self。
> - d2.add2(2) 输出结果为12，为什么不是19？因为我们显示的将 super 第一个参数传递为 C，那么将只从 A, object 查找 add 方法，从输出
> 结果可以看出来这点。

### 一些思考
1. 如果把 B 中的 `super().add(m)` 删除，`d1.add1(2)` 调用后的 `d1.n` 值是多少呢？<br>
答案：
```bash
self is <__main__.D object at 0x10714b8d0> @D.add1
self is <__main__.D object at 0x10714b8d0> @B.add
13 =================
```

从这个问题看出，要让 super 按正常的 MRO 顺序炒作某个方法，父类的方法都必须通过 super 正确关联。

2. 如果把 B 中的 `super().add(m)` 删除，`d1.add2(2)` 调用后的 `d2.n` 值是多少呢？<br>
答案：
```bash
self is <__main__.D object at 0x10714b668> @D.add2
self is <__main__.D object at 0x10714b668> @A.add
12 =================
```
从这个问题看出，某个父类的 super 查找中断，并不影响从其后开始正常查找。所谓正常查找，就是其后的父类方法都通过 super 正确
关联了。

3. 在 `__new__` 方法中调用无参数 `super()` 会有什么结果<br>
答案:   
会抛出异常 `TypeError: object.__new__(): not enough arguments`。这是因为__new__是一个类方法，还不存在对应的实例对象。如果
在 `classmethod`装饰器修饰的类方法上调用 `super`, 则抛出异常 `TypeError: add() missing 1 required positional argument: 'm'`。
原因和这个差不多。
