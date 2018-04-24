Title: Python 异常问题汇总
Date： 2018-04-24 11：20
category: python
tags: Python 异常

#### 问题一：TypeError: object() takes no parameters

最近在测试 Python 的 `__new__` 方法时，我写了如下验证代码

```python
class test(object):
    def __init__(self, a):
        print("this is a init method")
        self.a = a

    def __new__(cls, *args, **kwargs):
        print("this is a new method")
        return super(test, cls).__new__(cls, *args, **kwargs)


t = test(12)
print(t.a)
```

结果在 Python2 运行正常，在 Python3 却报如下异常

```shell
this is a new method
Traceback (most recent call last):
  File "test.py", line 11, in <module>
    t = test(12)
  File "test.py", line 8, in __new__
    return super(test, cls).__new__(cls, *args, **kwargs)
TypeError: object() takes no parameters
```

一开始是以为 `__init__` 拼写错误，或者 tab，spec 混用导致，但是 `t = test()` 却提示需要传递参数 a

```shell
this is a new method
Traceback (most recent call last):
  File "test.py", line 11, in <module>
    t = test()
TypeError: __init__() missing 1 required positional argument: 'a'
```

那这样就纳闷了，竟然可以找到自己的 `__init__` 方法，那为什么还报 no parameters 呢。

----------
这是分割线。后面我查询了很久，在 stackoverflow 找到了回答
https://stackoverflow.com/questions/34777773/typeerror-object-takes-no-parameters-after-defining-new`   

下面是 @Blckknght 的回答

>In Python 3.3 and later, if you're overriding both \_\_new\_\_ and \_\_init\_\_, you need to avoid passing any extra arguments to the object methods you're overriding. 
>If you only override one of those methods, it's allowed to pass extra arguments to the other one (since that usually happens without your help).

将我的测试代码` __new__` 方法部分改成如下

```python
def __new__(cls, *args, **kwargs):
    print("this is a new method")
    return super(test, cls).__new__(cls)   # 不需要传递额外的参数
```
这样就可以运行成功了。  

那我不禁要问，Python3.3+ 到底怎么调用 `__init__` 方法的呢，上面的回答也答复了。`__init__` 调用是通过 `type.__call__`，那么 `object.__new__` 自然不需要知道 `__init__`  的额外参数   

感谢 @Blckknght 的回答！！！
