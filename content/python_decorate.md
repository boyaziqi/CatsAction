Title: python生成器
Date: 2017-04-05 17:50
Modified: 2017-04-06 15:30
category:  python
tags: python生成器

生成器的定义就不冗述了，它可以是函数，也可以是类。可以带参数。接下来分别介绍：
<br>

#### 1：不带参数的生成器（函数）
```python
def decorate(func):
    def wrapper(*args, **kwargs):
        print("this is a decorate")
        func(*args, **kwargs)
    return wrapper

@decorate
def test():
    print("this is test")

test()
```
*注意：调用方式是@decorate，后面不跟括号，加上括号就成调用带参数的生成器了。相当于`test = decorate(test)`。输出结果为：*
```
this is a decorate
this is test
```
<br>

#### 2：带参数的生成器（函数）
```python
#!/usr/env/bin python

def decorate(parameter=None):
    def dec(func):
        def wrapper(*args, **kwargs):
            print(parameter)
            func(*args, **kwargs)
        return wrapper
    return dec

@decorate("have parameter decorate")
def test():
    print("this is test")


test()
```
python解释器会自动识别封装，将函数传递给dec。相当于`test = decorate("have parameter decorate")(func)`.输出结果为：
```
have parameter decorate
this is test
```
<br>

#### 3：类装饰器
```python
class decorate(object):
    def __init__(self, func):
        print("this is a class decorate")
        self._func = func
        func(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        self._func(*args, **kwargs)
```
*调用方式为@decorate, 函数会被传递给__init__方法，返回一个类实例，当实例被调用时，也就是执行__call__方法*

如果类装饰器初始化的时候想初始化一些变量，可以在__init__方法中完成，实例如下：
```python
class decorate(object):
    def __init__(self, name, date):
        self._name = name
        self._date = date
    def __call__(self, func):
        def wrap(*args, **kwargs):
            print(self._name, self._date)
            func(*args, **kwargs)
        return wrap
```
*调用方式为@decorate("test", "2017-04-06"), python解释器会先把参数传给__init__初始化实例，再调用__call__返回装饰后的函数。*

{cat}fanxu
