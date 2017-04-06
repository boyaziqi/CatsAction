Title: python生成器
Date: 2017-04-05 17:50
Modified: 2017-04-06 15:30
category:  技术博文
tags: 闲谈，python

生成器的定义就不冗述了，它可以是函数，也可以是类。可以带参数。接下来分别介绍：

#### 1：不带参数的生成器（函数）
````python
def decorate(func):
    def wrapper(*args, **kwargs):
        print("this is a decorate")
        func(*args, **kwargs)
    return wrapper

@decorate
def test():
    print("this is test")

test()
````
*注意：调用方式是@decorate，后面不跟括号，加上括号就成调用带参数的生成器了。相当于`test = decorate(test)`。输出结果为：*
```
this is a decorate
this is test
```

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

### 3：类装饰器
```python
class decorate(object):
    def __init__(self, func):
        print("this is a class decorate")
        func(*args, **kwargs)
```
